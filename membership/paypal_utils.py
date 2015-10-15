from django.core.urlresolvers import reverse

import string, random, datetime
from six import text_type
from six.moves.urllib.parse import urlencode


def paypal_post(self,params):
  CHARSET = "windows-1252"
  cond_encode = lambda v: v.encode(CHARSET) if isinstance(v, text_type) else v
  byte_params = {cond_encode(k): cond_encode(v) for k, v in params.items()}
  post_data = urlencode(byte_params)
  ipn_url = reverse("paypal-ipn")
  return self.client.post(ipn_url, post_data, content_type='application/x-www-form-urlencoded')

def randstring(number):
  seed = string.letters[-26:]+string.digits
  return ''.join([random.choice(seed) for i in range(number)])

def get_paypal_query(**kwargs):
  kwargs['txn_id'] = kwargs.get('txn_id',None) or randstring(19)
  kwargs['payment_date'] = kwargs.get('payment_date',datetime.datetime.now()).strftime('%H:%M:%S %b %d, %Y PDT')

  user = kwargs.pop('user',None)
  if user:
    kwargs['first_name'] = kwargs.get('first_name') or user.first_name
    kwargs['last_name'] = kwargs.get('last_name') or user.last_name
    kwargs['payer_email'] = kwargs.get('payer_email') or user.payer_email
  defaults = {
    # unique to every purchase
    'txn_id': None,
    'payment_date': None,
    'txn_type': 'subscr_payment',

    # cart details should be covered in a function that calls this
    #'mc_gross': '25.00',
    #'payment_gross': '25.00',
    #'item_name': 'Tinkerer Membership Subscribe',
    #'transaction_subject': 'Tinkerer Membership Subscribe',

    # untouched variables
    'receiver_email': 'txrxlabs@gmail.com',
    'payment_status': 'Completed',
    'residence_country': 'US',
    'payer_status': 'verified',
    'charset': 'windows-1252',
    'notify_version': '3.8',
    'receiver_id': 'N7QDT9TLF3MEE',
    'business': 'txrxlabs@gmail.com',
    'payer_id': '35PHGV6AXP3GL',
    'verify_sign': 'A5e9lV2PGcJ2TfvuDc29WKkiqC8YA9rzf9LlbSeZjRDjXgPzQS14GvMq',
    'payment_fee': '0.85',
    'mc_fee': '0.85',
    'mc_currency': 'USD',
    'payment_type': 'instant',
    'ipn_track_id': 'ebaee57432f4f',
    'protection_eligibility': 'Ineligible',
  }
  defaults.update(**kwargs)
  return defaults

def get_membership_query(**kwargs):
  product = kwargs.pop('product')
  kwargs['subscr_id'] = kwargs.get('subscr_id',None) or "I-"+randstring(12)
  kwargs['mc_gross'] = kwargs.get('mc_gross',None) or product.unit_price
  kwargs['payment_gross'] = kwargs['mc_gross']
  kwargs['item_name'] = kwargs['transaction_subject'] = unicode(product)
  kwargs['option_name1'] = unicode(product.level)
  return get_paypal_query(**kwargs)

def get_course_query(**kwargs):
  # additionally custom can be passed in which is either an email or a user.pk
  sessions = kwargs.pop('sessions',[kwargs.pop('session')])
  quantities = kwargs.pop('quantities',[1]*len(sessions))
  kwargs['num_cart_items'] = len(sessions)
  kwargs['txn_type'] = 'cart'
  for i,session in enumerate(sessions):
    n = i + 1
    quantity = quantities[i]
    kwargs['item_name%s'%n] = session.course.name
    kwargs['quantity%s'%n] = quantity
    kwargs['mc_gross_%s'%n] = quantity*session.course.fee
    kwargs['item_number%s'%n] = session.pk
  return get_paypal_query(**kwargs)

def get_flag_query(txn_type,**kwargs):
  kwargs['subscr_id'] = kwargs.get('subscr_id',None) or "I-"+randstring(12)
  kwargs['txn_type'] = txn_type
  return get_paypal_query(**kwargs)
