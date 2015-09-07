import requests, urlparse, datetime, django, os, random
from functools import wraps
os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'
django.setup()
from django.conf import settings
from django.db import reset_queries
from paypal.standard.ipn.models import PayPalIPN
from course.models import Enrollment, Session
from course.utils import get_or_create_student
from user.models import User
from membership.models import Subscription, Status, Membership, MembershipProduct, UserMembership

#[s.recalculate() for s in Subscription.objects.all()];exit()
Status.objects.all().delete()
Subscription.objects.all().delete()
UserMembership.objects.all().update(end=None)

def cache_output(file_name):
  """Save the output of the function as file_name"""
  def decorator(method):
    @wraps(method)
    def wrapper(*args,**kwargs):
      if os.path.exists(file_name):
        with open(file_name,'r') as f:
          return eval(f.read())
      output = method(*args,**kwargs)
      with open(file_name,'w') as f:
        f.write(repr(output))
        print "wrote ",file_name
      return output
    return wrapper
  return decorator

requests.packages.urllib3.disable_warnings()

BASE_URL = "https://api-3t.paypal.com/nvp?USER=%s&PWD=%s&SIGNATURE=%s&VERSION=124"
BASE_URL = BASE_URL%(settings.PP_USERNAME,settings.PP_PASSWORD,settings.PP_SIGNATURE)

def get_txn_ids_for_day(day):
  starts = day.strftime("%Y-%m-%dT00:00:00Z")
  ends = (day+datetime.timedelta(1)).strftime("%Y-%m-%dT00:00:00Z")
  Q = "&METHOD=TransactionSearch&STARTDATE=%s&ENDDATE=%s"%(starts,ends)
  r = requests.get(BASE_URL+Q)
  raw_d = urlparse.parse_qs(r.text)
  return [v[0] for k,v in raw_d.items() if k.startswith("L_TRANSACTIONID")]

def get_subscription_info(subscr_id):
  Q = "&METHOD=GetRecurringPaymentsProfileDetails&PROFILEID=%s"%subscr_id
  r = requests.get(BASE_URL+Q)
  raw_d = r.text
  print r.text

num_years = 5

@cache_output('_%sppt.txt'%num_years)
def get_txn_ids():
  ids = []
  for i in range(365*num_years+90)[::-1]:
    d = datetime.date.today()-datetime.timedelta(i)
    # this next line is better since it isn't a relative date
    ids += cache_output("txn_ids/%s.%s.%s.day"%(d.year,d.month,d.day))(lambda: get_txn_ids_for_day(d))()
  return ids

def get_txn(txn_id):
  ipn = PayPalIPN.objects.filter(txn_id=txn_id)
  Q = "&METHOD=GetTransactionDetails&TRANSACTIONID=%s"%txn_id
  r = requests.get(BASE_URL+Q)
  raw_d = urlparse.parse_qs(r.text)
  return raw_d

def get_cart_item(d,key,i):
  return d.get('L_%s%s'%(key,i),[None])[0]

def process_cart(d,user,txn_id=None,**kwargs):
  return
  for i in range(10):
    if not get_cart_item(d,'AMT',i):
      break
    amt = get_cart_item(d,'AMT',i)
    name = get_cart_item(d,'NAME',i)
    number = get_cart_item(d,'NUMBER',i)
    qty = get_cart_item(d,'QTY',i)
    if not number.isdigit() or not Session.objects.filter(pk=number):
      continue
    session = Session.objects.get(pk=number)
    if not session.course.name in name:
      print "name mismatch:\n%s\n%s\n"%(session.course.name,name)

opt_names = {}
amts = {}
monthly = {}
yearly = {}

strptime = lambda s: datetime.datetime.strptime(s,"%Y-%m-%dT%H:%M:%SZ")

"""
Non-paying Member
TX/RX Supporter
Amigotron
Tinkerer
Hacker
Table Hacker
"""
membership_map = {
  "Artist": 'Tinkerer',
  "Crafter": 'Hacker',
  "Table Artist": 'Table Hacker',
  "Full Member Subscribe": 'Hacker',
  "Full Membership": 'Hacker',
  "Full Membership Dual": 'Hacker',
  "Auto Membership": "Hacker",
  #"Hacker": '',
  "Mike Reynolds Membership": 'Hacker',
  "Special Full Bay Memberhip Tiny House Build": 'Table Hacker',
  #"Table Hacker": '',
  "Table": "Table Hacker",
  "Table Membership": 'Table Hacker',
  "Table Membership (1/2 Bay)": 'Table Hacker',
  "Table Membership (1/4 Bay Legacy)": 'Table Hacker',
  #"Tinkerer": '',
  "Tinkerer (Monthly Legacy)": 'Tinkerer',
  #"TX/RX Supporter": ''
}

membership_lookup = {
  'Amigotron': [110,220],#['20.00', '10.00'], ['110.00', '220.00']],
  'TX/RX Supporter': [110],
  'Tinkerer': [225,250,440,275,550],
  'Hacker': [500,800,880,990,275],
  'Table Hacker': [1815,1595, 1200],
}

membership_skips = ['Auto Membership', 'Table']

def process_subscrpayment(d,user,txn_id=None,subscr_id=None,**kwargs):
  if subscr_id in ['I-CY935RUG8XY2','I-NSJ6LKWJ7TB6']:
    continue
  for i in [0]:
    if random.random() > 0.99:
      reset_queries()
    name = get_cart_item(d,'OPTIONSNAME',i) or d.get('SUBJECT',[''])[0].replace(' Membership Subscribe','')
    name = name.replace(" (One-Year Legacy)","")
    value = get_cart_item(d,'OPTIONSVALUE',i)
    if not name:
      break
    ordertime = strptime(d.get("ORDERTIME")[0])
    amt = d.get("AMT")[0]
    if not name in opt_names:
      opt_names[name] = datetime.datetime(2000,1,1)
      amts[name] = []
    if opt_names[name] < ordertime:
      opt_names[name] = ordertime
    if not amt in amts[name]:
      amts[name].append(amt)
    membership_name = membership_map.get(name,name)
    try:
      membership = Membership.objects.get(name=membership_name)
    except Membership.DoesNotExist:
      print '"%s" membership not found: $%s %s - %s'%(membership_name,amt,d['EMAIL'][0],ordertime)
      break
    _d = monthly
    amt = int(float(amt))
    #if amt == 270:
    #  print sorted(d.items())
    months = 1
    if amt in membership_lookup[membership_name]:
      _d = yearly
      months = 12
    if not membership_name in _d:
      _d[membership_name] = []
    if not amt in _d[membership_name]:
      _d[membership_name].append(amt)
    try:
      product = MembershipProduct.objects.filter(membership__name=membership_name,months=months)[0]
    except IndexError:
      print "Cannot find %s @ %s"%(membership_name,months)
      return
    defaults = {'product': product, 'created': ordertime,'user': user, 'amount': amt}
    subscription, new = Subscription.objects.get_or_create(subscr_id=subscr_id,defaults=defaults)
    if subscription.created > ordertime:
      subscription.created = ordertime
      subscription.save()
    if new:
      print "%s created subscription %s"%(subscr_id,ordertime)
    Status.objects.get_or_create(
      subscription=subscription,
      amount=amt,
      datetime=ordertime,
      payment_method='legacy',
    )
    return name

processors = {
  'cart': process_cart,
  #'refund': ,#279
  'subscrpayment': process_subscrpayment,#3930
  #'recurring_payment': ,#15
  #'sendmoney': ,#40
  #'reversal': ,#12
  #'webaccept': ,#60
  #'expresscheckout': ,#47
}

status_processors = ['Completed','Refunded','PartiallyRefunded','Failed']
if __name__ == "__main__":
  ids = get_txn_ids()
  found = 0
  missing = 0
  types = {}
  users = User.objects.all().count()
  for i in ids:
    if i.startswith('I-'):
      continue
    d = cache_output("txn_ids/%s"%i)(lambda: get_txn(i))()
    if not 'TRANSACTIONTYPE' in d:
      continue
    txn_type = d['TRANSACTIONTYPE'][0]
    if not txn_type in types:
      pass #print txn_type,': ',d.keys()
    types[txn_type] = types.get(txn_type,0) + 1
    subscr_id = d.get("SUBSCRIPTIONID",[None])[0]
    txn_id = d.get("TRANSACTIONID",[None])[0]
    email = d.get("EMAIL",[None])[0]
    if txn_type == 'subscrpayment' and not d['PAYMENTSTATUS'][0] in status_processors:
      print "bad status: ",d['PAYMENTSTATUS'][0]
      continue
    if PayPalIPN.objects.filter(txn_id=txn_id):
      continue
    user,new = get_or_create_student(email,subscr_id=subscr_id,send_mail=False)
    if new:
      print '\t'.join([str(s) for s in [txn_type[:6],subscr_id,email,user]])
    if not txn_type in processors:
      continue
    processors[txn_type](d,user,txn_id=txn_id,subscr_id=subscr_id)
  #for k,v in types.items():
  #  print k,':  ',v
  for k in sorted(opt_names.keys()):
    print k,':  ',opt_names[k],' ',sorted(amts[k])
  print "Monthly"
  for k,v in sorted(monthly.items()):
    print k,':  ',v
  print "Yearly"
  for k,v in sorted(yearly.items()):
    print k,':  ',v
  
