from django.core.management.base import BaseCommand
from django.core.mail import send_mail,mail_admins
from django.conf import settings

import datetime,calendar, traceback

from event.models import EventRepeat

class Command (BaseCommand):
  def handle(self, *args, **options):
    for er in EventRepeat.objects.all():
      old_count = er.eventoccurrence_set.all().count()
      er.generate()
      new_count = er.eventoccurrence_set.all().count()
      if old_count != new_count:
        print "New Events Repeated: %s of %s"%(new_count-old_count,er)
