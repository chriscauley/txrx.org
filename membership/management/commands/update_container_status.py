from django.core.management.base import BaseCommand

from membership.models import Container

from lablackey.mail import print_to_mail
import datetime

class Command(BaseCommand):
  @print_to_mail(subject='Container Statuses',notify_empty=lambda:False)
  def handle(self, *args, **options):
    for container in Container.objects.all():
      status = container.status
      container.save() # Triggers update_status
      if status != container.status:
        print "%s@%s status changed from %s to %s"%(container.subscription,container,status,container.status)
