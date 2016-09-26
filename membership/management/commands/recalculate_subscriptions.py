from django.conf import settings
from django.core.management.base import BaseCommand

from membership.models import Subscription

class Command(BaseCommand):
  def handle(self, *args, **options):
    #We don't care about canceled subscriptions that have been set to 0 owed and users reset to non-paying
    ss = Subscription.objects.exclude(canceled__isnull=True,user__level=settings.DEFAULT_MEMBERSHIP_LEVEL,owed=0)
    print "Calculating %s subscriptions"%ss.count()
    for s in ss:
      s.recalculate()
    print "%s subscriptions remain"%ss.count()
