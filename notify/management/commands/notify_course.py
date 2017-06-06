from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.mail import mail_admins
from django.template.defaultfilters import striptags, date
from django.template.loader import render_to_string

from course.models import Session
from lablackey.contenttypes import get_contenttype
from lablackey.mail import send_template_email
from main.var import admin_comment_email, comment_response_email
from membership.models import LimitedAccessKey
from notify.models import Notification

import datetime

class Command (BaseCommand):
  def handle(self, *args, **options):
    # First people who are following classes
    notifications = Notification.objects.filter(emailed__isnull=True,target_type='course.session')
    students = get_user_model().objects.filter(id__in=set(notifications.values_list("user",flat=True)))
    count = 0
    users_count = len(students)
    if not users_count and not settings.TESTING:
      mail_admins("No classes","No new classes to notify anyone about :(")
    for user in students:
      notifications = user.notification_set.filter(emailed__isnull=True,target_type="course.session")
      count += notifications.count()
      sessions = [n.target for n in notifications]
      _dict = {
        'user': user,
        'la_key': LimitedAccessKey.new(user),
        'new_sessions': sessions,
        'notifications': notifications,
      }
      if user.notifysettings.new_sessions == "email":
        send_template_email("notify/email/course",[user.email],context=_dict)
      elif user.notifysettings.new_sessions == "sms":
        c = sessions[0].course.get_short_name()
        p = ""
        if len(sessions) > 1:
          p = " and %s other classes you are interested in"%(len(sessions) - 1)
        m = "There a new session of %s%s at %s. Visit %s to find out more"

        user.send_sms(m%(c,p,settings.SITE_NAME,settings.NOTIFY_URL))
      notifications.update(emailed=datetime.datetime.now())
    # Now hit up enrollments that are happening tomorrow
    for relationship in ["teaching_reminder","course_reminder"]:
      _notifications = Notification.objects.filter(emailed__isnull=True,target_type="course.classtime")
      _notifications = _notifications.filter(relationship=relationship)
      followers = get_user_model().objects.filter(id__in=set(_notifications.values_list("user",flat=True)))
      users_count = len(followers)
      for user in followers:
        notifications = user.notification_set.filter(
          emailed__isnull=True,
          target_type="course.classtime",
          relationship=relationship,
        )
        count += notifications.count()
        classtimes = sorted([n.target for n in notifications],key=lambda ct: ct.start)
        if user.notifysettings.my_classes == "email":
          _dict = {
            'user': user,
            'la_key': LimitedAccessKey.new(user),
            'SITE_URL': settings.SITE_URL,
            'notifications': notifications,
            'first_classtime': classtimes[0],
            'classtimes': classtimes
          }
          send_template_email("email/%s"%relationship,[user.email,'chris@lablackey.com'],context=_dict)
        elif user.notifysettings.my_classes == "sms":
          course_name = classtimes[0].session.course.get_short_name()
          time_s = date(classtimes[0].start,"P")
          if len(classtimes) == 1:
            body = "You have class tomorrow at %s: %s @ %s"%(settings.SITE_NAME,course_name,time_s)
          else:
            body = "You have %s classes tomorrow at %s. The first is: %s @ %s"%(len(classtimes),settings.SITE_NAME,course_name,time_s)
          user.send_sms(body)

        notifications.update(emailed=datetime.datetime.now())
      if options.get("verbosity") > 0:
        print "%s: Notified %s users of %s notifications"%(relationship,users_count,count)
