from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from course.models import Enrollment
from lablackey.mail import mail_on_fail
from membership.models import LimitedAccessKey

import datetime

class Command (BaseCommand):
  @mail_on_fail
  def handle(self, *args, **options):
    yesterday = datetime.datetime.now()-datetime.timedelta(7)
    pe = Enrollment.objects.pending_evaluation()
    pe = pe.filter(evaluation_date__gte=yesterday)
    if pe.count() and options.get("verbosity") > 0:
      print "sending %s evaluation emails"%pe.count()
    for enrollment in pe:
      if not enrollment.user.email:
        continue
      _dict = {
        'evaluation': enrollment,
        'la_key': LimitedAccessKey.new(enrollment.user),
        'domain': settings.SITE_URL,
        'settings': settings
      }
      subject = "Please evaluate the class you took from %s"%settings.SITE_NAME
      if enrollment.session.course.get_private_files():
        subject = "Course files and pending evaluation for %s"%enrollment.session.course
      send_mail(
        subject,
        render_to_string("email/pending_evaluation.html",_dict),
        settings.DEFAULT_FROM_EMAIL,
        [enrollment.user.email]
      )
      enrollment.emailed=True
      enrollment.save()
