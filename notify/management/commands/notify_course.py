from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.template.defaultfilters import striptags
from django.template.loader import render_to_string

from course.models import Session
from txrx.mail import send_mail_plus, mail_admins_plus, filter_users
from txrx.utils import mail_on_fail
from membership.models import LimitedAccessKey

import datetime

class Command (BaseCommand):
  #@mail_on_fail
  def handle(self, *args, **options):
    dt = datetime.datetime.now()-datetime.timedelta(2)
    new_sessions = Session.objects.filter(created__gte=dt,first_date__gte=datetime.datetime.now())

    if not new_sessions:
      mail_admins_plus("No classes","No new classes to email anyone about :(")
      return
    courses = list(set([s.section.course for s in new_sessions]))
    users = User.objects.filter(notifycourse__course__in=courses).distinct()
    for user in users:
      sessions = [s for s in new_sessions if user.notifycourse_set.filter(course=s.section.course)]
      _dict = {
        'user': user,
        'la_key': LimitedAccessKey.new(user),
        'SITE_URL': settings.SITE_URL,
        'new_sessions': sessions,
        }
      send_mail_plus(
        "[TX/RX] New classes at the hackerspace",
        render_to_string("notify/notify_course.html",_dict),
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        )
