from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import QueryDict
from lablackey.utils import get_or_none

from course.utils import get_or_create_student
from .models import UserMembership, Status, Subscription, Membership, Product
from user.models import User

from paypal.standard.ipn.signals import payment_was_successful, payment_was_flagged, subscription_signup

@receiver(post_save,sender=User)
def post_save_user_handler(sender, **kwargs):
  user = kwargs['instance']
  UserMembership.objects.get_or_create(user=user)

_duid2='membership.listners.membership_payment'
@receiver(payment_was_flagged, dispatch_uid=_duid2)
@receiver(subscription_signup, dispatch_uid=_duid2)
@receiver(payment_was_successful, dispatch_uid=_duid2)
def membership_payment(sender,**kwargs):
  if sender.txn_type != "subscr_payment":
    return # not a membership payment
  if Status.objects.filter(paypalipn=sender):
    return # This has already been processed
  params = QueryDict(sender.query)
  subscr_id=params.get('subscr_id',None)
  user,new_user = get_or_create_student(sender.payer_email,subscr_id=subscr_id)
  subscription = get_or_none(Subscription,subscr_id=subscr_id)
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
