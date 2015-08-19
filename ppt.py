import requests, urlparse, datetime, django, os
from functools import wraps
os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'
django.setup()
from django.conf import settings
from paypal.standard.ipn.models import PayPalIPN
from course.models import Enrollment, Session
from course.utils import get_or_create_student
from user.models import User

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

@cache_output('__ppt.txt')
def get_txn_ids():
  ids = []
  for i in range(600):
    ids += get_txn_ids_for_day(datetime.date.today()-datetime.timedelta(i))
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
  for i in range(10):
    if not get_cart_item(d,'AMT',i):
      break
    amt = get_cart_item(d,'AMT',i)
    name = get_cart_item(d,'NAME',i)
    number = get_cart_item(d,'NUMBER',i)
    qty = get_cart_item(d,'QTY',i)
    if not Session.objects.filter(pk=number):
      continue
    session = Session.objects.get(pk=number)
    if not session.course.name in name:
      pass #print "name mismatch:\n%s\n%s\n"%(session.course.name,name)

opt_names = {}

strptime = lambda s: datetime.datetime.strptime(s,"%Y-%m-%dT%H:%M:%SZ")

def process_subscrpayment(d,user,txn_id=None,subscr_id=None,**kwargs):
  for i in [0]:
    name = get_cart_item(d,'OPTIONSNAME',i) or d.get('SUBJECT',[''])[0].replace(' Membership Subscribe','')
    value = get_cart_item(d,'OPTIONSVALUE',i)
    if not name:
      print d
      break
    ordertime = strptime(d.get("ORDERTIME")[0])
    if not name in opt_names:
      opt_names[name] = datetime.datetime(2000,1,1)
    if opt_names[name] < ordertime:
      opt_names[name] = ordertime

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
if __name__ == "__main__":
  ids = get_txn_ids()
  found = 0
  missing = 0
  types = {}
  users = User.objects.all().count()
  for i in ids:
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
    if PayPalIPN.objects.filter(txn_id=txn_id):
      continue
    user,new = get_or_create_student(email,subscr_id=subscr_id,send_mail=False)
    if new:
      print '\t'.join([str(s) for s in [txn_type[:6],subscr_id,email,user]])
    if txn_type in processors:
      processors[txn_type](d,user,txn_id=txn_id,subscr_id=subscr_id)
  for k,v in types.items():
    print k,':  ',v
  for k,v in opt_names.items():
    print k,':  ',v
