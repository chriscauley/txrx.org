from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import QueryDict

from course.utils import get_or_create_student
from .models import UserMembership, MembershipChange, Membership, MembershipProduct
from user.models import User

from paypal.standard.ipn.signals import payment_was_successful, subscription_signup

@receiver(post_save,sender=User)
def post_save_user_handler(sender, **kwargs):
  user = kwargs['instance']
  UserMembership.objects.get_or_create(user=user)

_duid2='membership.listners.handle_successful_membership_payment'
@receiver(payment_was_successful, dispatch_uid=_duid2)
def handle_successful_membership_payment(sender,**kwargs):
  if sender.txn_type != "subscr_payment":
    return # not a membership payment
  if MembershipChange.objects.filter(transaction_id=sender.txn_id):
    return # This has already been processed
  params = QueryDict(sender.query)
  user,new_user = get_or_create_student(sender.payer_email,subscr_id=params.get('subscr_id',None))
  try:
    membership = Membership.objects.get(name=params.get('option_name1',''))
  except Membership.DoesNotExist:
    b = "Could not find membership %s for txn %s"%(params.get('option_name1',''),sender.txn_id)
    mail_admins("Bad IPN",b)
    return
  if not 'mc_gross' in params:
    mail_admins("Bad IPN","no mc_gross in txn %s"%sender.txn_id)

  try:
    product = MembershipProduct.objects.get(unit_price=params['mc_gross'],membership=membership)
  except MembershipProduct.DoesNotExist:
    b = "Could not find membership product %s $%s for txn %s"
    mail_admins("Bad IPN",b%(membership,params['mc_gross'],sender.txn_id))
    return
  MembershipChange.objects.create(
    user = user,
    membershipproduct = product,
    transaction_id = sender.txn_id,
    subscr_id = params.get(subscr_id),
    payment_method='paypal',
    paypalipn=sender
  )

_duid2='membership.listners.handle_subscription_signup'
@receiver(subscription_signup, dispatch_uid=_duid2)
def handle_subscription_signup(sender,**kwargs):
  if sender.txn_type != "subscr_payment":
    print "\n\n\nNOT A SUBSCRIPTION PAYMENT\n\n\n"
    return # not a membership payment
  if MembershipChange.objects.filter(transaction_id=sender.txn_id):
    return # This has already been processed
  params = QueryDict(sender.query)
  user,new_user = get_or_create_student(sender.payer_email,subscr_id=params.get('subscr_id',None))
  try:
    membership = Membership.objects.get(name=params.get('option_name1',''))
  except Membership.DoesNotExist:
    b = "Could not find membership %s for txn %s"%(params.get('option_name1',''),sender.txn_id)
    mail_admins("Bad IPN",b)
    return
