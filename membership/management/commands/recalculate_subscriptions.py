from django.conf import settings
from django.core.management.base import BaseCommand

from membership.models import Subscription

class Command(BaseCommand):
  def handle(self, *args, **options):
    #We don't care about canceled subscriptions that have been set to 0 owed and users reset to non-paying
    ss = Subscription.objects.exclude(canceled__isnull=False,user__level=settings.DEFAULT_MEMBERSHIP_LEVEL,owed=0)
    old_count = ss.count()
    for s in ss:
      s.recalculate()
    if options.get("verbosity") > 0:
      print "Calculating %s subscriptions"%old_count
      print "%s subscriptions remain"%ss.count()
