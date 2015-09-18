from django.core.mail import mail_admins
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import QueryDict
from lablackey.utils import get_or_none

from course.utils import get_or_create_student
from .models import UserMembership, Status, Subscription, Membership, Product, SubscriptionFlag
from user.models import User

from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received

@receiver(post_save,sender=User)
def post_save_user_handler(sender, **kwargs):
  user = kwargs['instance']
  UserMembership.objects.get_or_create(user=user)

def get_subscription(params,sender):
  subscr_id = params.get('subscr_id',None) or params.get('recurring_payment_id',None)
  if not subscr_id:
    mail_admins("Bad IPN","no subscr_id in IPN #%s"%sender.pk)
    return
  subscription = get_or_none(Subscription,subscr_id=subscr_id)
  if not subscription:
    mail_admins("Bad IPN","no subscr_id in IPN #%s"%sender.pk)
    return
  return subscription

def paypal_flag(sender,reason=None,**kwargs):
  if not kwargs['subscription']:
    return
  SubscriptionFlag.objects.create(
    subscription=kwargs['subscription'],
    reason=reason or sender.txn_type,
  )

@receiver(valid_ipn_received,dispatch_uid='paypal_signal')
@receiver(invalid_ipn_received,dispatch_uid='paypal_signal')
def paypal_signal(sender,**kwargs):
  params = QueryDict(sender.query)
  subscr_id = params.get('subscr_id',None) or params.get('recurring_payment_id',None)
  if sender.txn_type in ['','cart','subscr_signup']:
    return # refunds and classes and signups
  if sender.txn_type != "subscr_payment":
    mail_admins('Unknown Transaction type "%s"'%sender.txn_type,
                "https://txrxlabs.org/admin/ipn/paypalipn/%s/"%sender.pk)
    return # rest of function handles successful membership payment
  if Status.objects.filter(paypalipn=sender):
    return # This has already been processed
  subscription = get_subscription(params,sender)
  kwargs['subscription'] = subscription
  user,new_user = get_or_create_student(sender.payer_email,subscr_id=subscr_id)

  if sender.txn_type in ['recurring_payment_skipped',"recurring_payment_failed","recurring_payment_suspended",
                         "subscr_failed"]:
    paypal_flag(sender,**kwargs)
    mail_admins("Flagged %s"%sender.txn_type,"https://txrxlabs.org/admin/membership/subscription/%s/"%subscription.pk)
    return
  elif sender.txn_type == 'subscr_eot':
    paypal_flag(sender,**kwargs)
    mail_admins("Flagged %s and canceled"%sender.txn_type,
                "https://txrxlabs.org/admin/membership/subscription/%s/"%subscription.pk)
    subscription.force_canceled()
    return
  elif sender.txn_type == 'subscr_cancel':
    if subscription:
      subscription.force_canceled()
      mail_admins("New Cancelation","https://txrxlabs.org/admin/membership/subscription/%s/"%subscription.pk)
    return

  if not 'mc_gross' in params:
    mail_admins("Bad IPN","no mc_gross in txn %s"%sender.txn_id)
    return
  amt = params['mc_gross']
  if not subscription:
    try:
      membership = Membership.objects.get(name=params.get('option_name1',''))
    except Membership.DoesNotExist:
      b = "Could not find membership %s for txn %s"%(params.get('option_name1',''),sender.txn_id)
      mail_admins("Bad IPN",b)
      return
    try:
      product = Product.objects.get(unit_price=amt,membership=membership)
    except Product.DoesNotExist:
      b = "Could not find membership product %s $%s for txn %s"
      mail_admins("Bad IPN",b%(membership,amt,sender.txn_id))
      return
    subscription = Subscription.objects.create(
      user=user,
      subscr_id=subscr_id,
      product=product,
      amount=amt
    )
  Status.objects.create(
    subscription=subscription,
    paypalipn=sender,
    payment_method='paypal',
    amount=amt,
  )
