from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.mail import mail_admins
from django.template.defaultfilters import striptags
from django.template.loader import render_to_string

from course.models import Session
from lablackey.contenttypes import get_contenttype
from lablackey.mail import send_template_email
from membership.models import LimitedAccessKey
from notify.models import Notification

import datetime

class Command (BaseCommand):
  def handle(self, *args, **options):
    users = get_user_model().objects.filter(notification__isnull=False)
    users = users.filter(notification__emailed__isnull=True).distinct()
    count = 0
    users_count = users.count()
    if not users_count:
      mail_admins("No classes","No new classes to notify anyone about :(")
      return
    for user in users:
      notifications = user.notification_set.filter(emailed__isnull=True)
      count += notifications.count()
      sessions = [n.target for n in notifications]
      _dict = {
        'user': user,
        'la_key': LimitedAccessKey.new(user),
        'new_sessions': sessions,
      }
      send_template_email("notify/email/course",[user.email],context=_dict)
      notifications.update(emailed=datetime.datetime.now())
    print "Notified %s users of %s notifications"%(len(users),count)
