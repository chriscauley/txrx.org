from django.core.management.base import BaseCommand

from membership.models import Subscription

class Command(BaseCommand):
  def handle(self, *args, **options):
    [s.recalculate() for s in Subscription.objects.all()]
    print "Calculated %s subscriptions"%Subscription.objects.count()
