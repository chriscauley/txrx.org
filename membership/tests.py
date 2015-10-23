from django.core import mail
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory

from .models import Product, Level, Group, add_months, Subscription, Flag
from .paypal_utils import get_membership_query, paypal_post, get_flag_query
from paypal.standard.ipn.models import PayPalIPN
from six import text_type
from six.moves.urllib.parse import urlencode

import datetime, urllib, os

import warnings
warnings.showwarning = lambda *x: None

BASE_URL = 'http://dev.txrxlabs.org:8025'

#this will be needed eventually, for now I just use the dev db
"""
def setUp():
  objects = [
    (Group,[
      {"name": "Non-Tool", "order": 3, 'pk': 1},
      {"name": "All Access", "order": 0, 'pk':3},
    ]),
    (Level,[
      {"discount_percentage": 0, "group": 1, "name": "Non-paying Member", "order": 0},
      {"discount_percentage": 10, "group": 3, "name": "Tinkerer", "order": 20},
      {"discount_percentage": 10, "group": 3, "name": "Hacker", "order": 21},
      {"discount_percentage": 10, "group": 3, "name": "Table Hacker", "order": 22},
      {"discount_percentage": 0, "group": 1, "name": "TXRX Supporter", "order": 1},
      {"discount_percentage": 5, "group": 1, "name": "Amigotron", "order": 2},
    ]),
  ]
  for model,kwargs in objects:
    model.objects.create(**kwargs)
"""

class SimpleTest(TestCase):
  def test_flags(self):
    flag_transactions = [
      'recurring_payment_skipped',"recurring_payment_failed","recurring_payment_suspended",
      'recurring_payment_suspended_due_to_max_failed_payment',
      "subscr_failed",'subscr_eot']
    all_transactions = flag_transactions + [
      'cart','subscr_signup','web_accept','send_money'
    ]
    for txn_type in all_transactions:
      level = Level.objects.get(name="Hacker")
      product = level.product_set.all()[0]
      new_email = "new_email%s@txrxtesting.com"%product.pk
      get_user_model().objects.filter(email=new_email).delete()
      data = get_membership_query(product=product,payer_email=new_email)
      paypal_post(self,data)
      subscription = Subscription.objects.get(user__email=new_email)
      subscr_id = subscription.subscr_id


      # Now let's flag that account
      mail.outbox = []
      flag_data = get_flag_query(txn_type,payer_email=new_email,subscr_id=subscr_id)
      paypal_post(self,flag_data)
      subscription = Subscription.objects.get(user__email=new_email)
      subjects = [m.subject for m in mail.outbox]
      if txn_type in flag_transactions:
        if txn_type == 'subscr_eot':
          self.assertTrue('[TXRX_DEV]Flagged %s and canceled'%txn_type in subjects)
          self.assertTrue(subscription.canceled)
        else:
          self.assertTrue('[TXRX_DEV]Flagged %s'%txn_type in subjects)
          self.assertTrue(not subscription.canceled)
        flag = Flag.objects.get(subscription=subscription)
        self.assertEqual(flag.reason,txn_type)
        self.assertEqual(flag.status,'new')
  def test_flag_workflow(self):
    """
    Create a user with a subscription and move it back to the past due date.
    Run the requisite management command and make sure that they get flagged.
    Promote the flag three times and make sure the emails go out and the days_until logic works
    Make sure appropriate flags are resolved on payment.
    """
    pass
  def test_hacker_membership(self):
    now = datetime.datetime.now()
    def validate(email):
      user = get_user_model().objects.get(email=email)
      self.assertEqual(user.level,product.level)
      subscription = user.subscription_set.get()
      self.assertEqual(subscription.paid_until.date(),add_months(now.date(),subscription.product.months))
      self.assertTrue(subscription.owed <= 0)

    level = Level.objects.get(name="Hacker")
    for product in level.product_set.all():
      new_email = "new_email%s@txrxtesting.com"%product.pk
      get_user_model().objects.filter(email=new_email).delete()
      data = get_membership_query(product=product,payer_email=new_email)
      paypal_post(self,data)
      validate(new_email)

      # reposting the same data should not change anything
      paypal_post(self,data)
      validate(new_email)

    get_user_model().objects.get(email=new_email).delete()
    PayPalIPN.objects.filter(txn_id=data['txn_id']).delete()
