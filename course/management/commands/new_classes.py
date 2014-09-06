from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.template.defaultfilters import striptags
from django.template.loader import render_to_string

from course.models import Session
from txrx.utils import mail_on_fail
from membership.models import LimitedAccessKey

import datetime

class Command (BaseCommand):
  @mail_on_fail
  def handle(self, *args, **options):
    user = get_user_model()
    dt = datetime.datetime.now() + datetime.timedelta(-16)
    new_sessions = Session.objects.filter(created__gte=dt,first_date__gte=datetime.datetime.now())
    if not new_sessions:
      mail_admins("No classes","No new classes to email anyone about :(")
      return
    kwargs = dict(usermembership__notify_sessions=True,usermembership__notify_global=True)
    users = User.objects.filter(**kwargs)
    for user in users:
      _dict = {
        'user': user,
        'la_key': LimitedAccessKey.new(user),
        'SITE_URL': settings.SITE_URL,
        'new_sessions': new_sessions,
        }
      send_mail(
        "[TX/RX] New classes at the hackerspace",
        render_to_string("email/new_classes.html",_dict),
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        )
