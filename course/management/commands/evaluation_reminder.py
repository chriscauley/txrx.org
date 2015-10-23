from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from course.models import Enrollment
from lablackey.mail import print_to_mail
from membership.models import LimitedAccessKey

import datetime

class Command (BaseCommand):
  @print_to_mail(subject="Evaluation Reminder")
  def handle(self, *args, **options):
    yesterday = datetime.datetime.now()-datetime.timedelta(1)
    pe = Enrollment.objects.pending_evaluation()
    pe = pe.filter(evaluation_date__gte=yesterday)
    if pe.count:
      print "sending %s evaluation emails"%pe.count()
    for enrollment in pe:
      if not enrollment.user.email:
        continue
      _dict = {
        'evaluation': enrollment,
        'la_key': LimitedAccessKey.new(enrollment.user),
        'domain': settings.SITE_URL
      }
      send_mail(
        "Please evaluate the class you took from %s"%settings.SITE_NAME,
        render_to_string("email/pending_evaluation.html",_dict),
        settings.DEFAULT_FROM_EMAIL,
        [enrollment.user.email]
      )
      enrollment.emailed=True
      enrollment.save()
      
      print "Emailed %s about %s"%(enrollment.user.email,enrollment.session)
