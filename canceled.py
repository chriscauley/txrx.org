import requests, urlparse, datetime, django, os, random
from functools import wraps
os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'
django.setup()

from membership.models import Subscription, Membership, add_months

Subscription.objects.all().update(canceled=None)

now = datetime.datetime.now()
low = high = other = 0

for subscription in Subscription.objects.all():
  subscription.recalculate()

f = open("_cancels.txt",'r')
subscr_ids = f.read().split("\n")
for subscr_id in subscr_ids:
  try:
    Subscription.objects.get(subscr_id=subscr_id).force_canceled()
  except:
    print subscr_id,' not found'
f.close()

initial = Subscription.objects.filter(owed__gt=0).count()

for membership in Membership.objects.filter(order__gte=1):
  for subscription in Subscription.objects.filter(product__membership=membership,owed__gt=0):
    if membership.order in [1,2]: #amigotron/supporter
      low += 1
      subscription.force_canceled()
    elif (now - subscription.last_status.datetime).days > 365:
      high += 1
      subscription.force_canceled()
    elif subscription.user.subscription_set.filter(owed__lte=0).exclude(pk=subscription.pk):
      subscription.force_canceled()
      other += 1
  print membership,'\t',Subscription.objects.filter(product__membership=membership,owed__gt=0).count()

print 'pp:\t',len(subscr_ids)
print 'init:\t',initial
print 'low:\t',low
print 'high:\t',high
print 'other:\t',other
print 'remain:\t',Subscription.objects.filter(owed__gt=0).count()

cancel_all = False

if cancel_all:
  for s in Subscription.objects.filter(owed__gt=0):
    s.force_canceled()
