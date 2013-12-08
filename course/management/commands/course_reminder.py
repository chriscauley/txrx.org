from django.core.management.base import BaseCommand
from django.conf import settings
from django.template.loader import render_to_string

from course.models import ClassTime
from main.signals import send_mail_plus
from membership.models import LimitedAccessKey

import datetime

class Command (BaseCommand):
  def handle(self, *args, **options):
    today = datetime.datetime.now()
    tomorrow = datetime.datetime.now()+datetime.timedelta(1)
    class_times = ClassTime.objects.filter(start__gte=today,start__lte=tomorrow)
    for class_time in class_times:
      sent = []
      for enrollment in class_time.session.enrollment_set.all():
        user = enrollment.user
        _dict = {
          'user': user,
          'la_key': LimitedAccessKey.new(user),
          'SITE_URL': settings.SITE_URL,
          'session': class_time.session,
          'class_time': class_time,
          }
        if user.email in sent:
          continue
        sent.append(user.email)
        send_mail_plus(
          "[TX/RX] Class today!",
          render_to_string("email/course_reminder.html",_dict),
          settings.DEFAULT_FROM_EMAIL,
          [user.email],
          )
