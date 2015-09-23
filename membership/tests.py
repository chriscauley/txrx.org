from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory

from .models import Product, Membership, Group
from .paypal_utils import get_membership_query
from paypal.standard.ipn.views import ipn as ipn_view
from six import text_type
from six.moves.urllib.parse import urlencode

import datetime,urllib

BASE_URL = 'http://dev.txrxlabs.org:8025'

def setUp():
  objects = [
    (Group,[
      {"name": "Non-Tool", "order": 3, 'pk': 1},
      {"name": "All Access", "order": 0, 'pk':3},
    ]),
    (Membership,[
      {"discount_percentage": 0, "group": 1, "name": "Non-paying Member", "order": 0},
      {"discount_percentage": 10, "group": 3, "name": "Tinkerer", "order": 20},
      {"discount_percentage": 10, "group": 3, "name": "Hacker", "order": 21},
      {"discount_percentage": 10, "group": 3, "name": "Table Hacker", "order": 22},
      {"discount_percentage": 0, "group": 1, "name": "TX/RX Supporter", "order": 1},
      {"discount_percentage": 5, "group": 1, "name": "Amigotron", "order": 2},
    ]),
  ]
  for model,kwargs in objects:
    model.objects.create(**kwargs)

class SimpleTest(TestCase):
  def paypal_post(self, params):
    CHARSET = "windows-1252"
    cond_encode = lambda v: v.encode(CHARSET) if isinstance(v, text_type) else v
    byte_params = {cond_encode(k): cond_encode(v) for k, v in params.items()}
    post_data = urlencode(byte_params)
    ipn_url = reverse("paypal-ipn")
    return self.client.post(ipn_url, post_data, content_type='application/x-www-form-urlencoded')
  def setUp(self):
    self.factory = RequestFactory()
  #  setUp()
  def test_hacker_membership(self):
    product = Membership.objects.get(name="Hacker").monthly_product
    new_hacker_email = "new_email@txrxtesting.com"
    data = get_membership_query(product=product,payer_email=new_hacker_email)
    self.paypal_post(data)
    users = get_user_model().objects.filter(email=new_hacker_email)
    self.assertEqual(users.count(),1)
    users.delete()
