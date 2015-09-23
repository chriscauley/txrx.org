import string, random, datetime

def randstring(number):
  seed = string.letters[-26:]+string.digits
  return ''.join([random.choice(seed) for i in range(number)])

def get_paypal_query(**kwargs):
  kwargs['txn_id'] = kwargs.get('txn_id',None) or randstring(19)
  kwargs['payment_date'] = kwargs.get('payment_date',datetime.datetime.now()).strftime('%H:%M:%S %b %d, %Y PDT')

  defaults = {
    # unique to every purchase
    'txn_id': None,
    'payment_date': None,
    'txn_type': 'subscr_payment',

    # cart details
    'mc_gross': '25.00',
    'payment_gross': '25.00',
    'item_name': 'Tinkerer Membership Subscribe',
    'transaction_subject': 'Tinkerer Membership Subscribe',

    # user details
    'first_name': 'mark',
    'last_name': 'garrett',
    'payer_email': 'markiep00-two@yahoo.com',

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
