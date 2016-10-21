import requests, urlparse, datetime, django, os, random
from functools import wraps
os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'
django.setup()

from membership.models import Subscription, Level, add_months

Subscription.objects.all().update(canceled=None)

now = datetime.datetime.now()
low = high = changed = 0

for subscription in Subscription.objects.all():
  subscription.recalculate()

f = open("_cancels.txt",'r')
subscr_ids = f.read().split("\n")
for subscr_id in subscr_ids:
  try:
    Subscription.objects.get(subscr_id=subscr_id.strip()).force_canceled()
  except:
    print subscr_id.strip(),' not found'
f.close()

initial = Subscription.objects.filter(owed__gt=0).count()

for level in Level.objects.filter(order__gte=1):
  for subscription in Subscription.objects.filter(level=level,owed__gt=0):
    if level.order in [1,2]: #amigotron/supporter
      low += 1
      subscription.force_canceled()
    elif (now - subscription.last_status.datetime).days > 365:
      high += 1
      subscription.force_canceled()
    elif subscription.user.subscription_set.filter(owed__lte=0).exclude(pk=subscription.pk):
      subscription.force_canceled()
      changed += 1
  print level,'\t',Subscription.objects.filter(level=level,owed__gt=0).count()

print 'pp:\t',len(subscr_ids)
print 'init:\t',initial
print 'low:\t',low
print 'high:\t',high
print 'changed:\t',changed
print 'remain:\t',Subscription.objects.filter(owed__gt=0).count()

cancel_all = False

if cancel_all:
  for s in Subscription.objects.filter(owed__gt=0):
    s.force_canceled()
