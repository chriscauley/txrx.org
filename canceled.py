import requests, urlparse, datetime, django, os, random
from functools import wraps
os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'
django.setup()

from membership.models import Subscription, Membership, add_months

Subscription.objects.all().update(canceled=None)

now = datetime.datetime.now()

for membership in Membership.objects.filter(order__gte=1):
  for subscription in Subscription.objects.filter(product__membership=membership):
    if membership.order in [1,2]: #amigotron/supporter
      subscription.recalculate()
      if subscription.owed > 0:
        subscription.force_canceled()
    else:
      last = subscription.last_status
      if (now - last.datetime).days > 365:
        subscription.force_canceled()

cancel_all=True

if cancel_all:
  for s in Subscription.objects.filter(owed__gt=0):
    s.force_canceled()
