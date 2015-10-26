from django.conf import settings
from django.core.mail import send_mail,mail_admins
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from course.models import ClassTime
from membership.models import LimitedAccessKey

from lablackey.mail import print_to_mail

import datetime

class Command(BaseCommand):
  @print_to_mail(subject="Course reminders")
  def handle(self, *args, **options):
    tomorrow = datetime.datetime.now().replace(hour=6)+datetime.timedelta(1)
    next_day = tomorrow + datetime.timedelta(1)
    class_times = ClassTime.objects.filter(start__gte=tomorrow,start__lte=next_day)
    if not class_times:
      return
    print "showing classes from %s to %s"%(tomorrow,next_day)
    print "reminding %s class times"%len(class_times)
    instructor_count = 0
    student_count = 0
    for class_time in class_times:
      instructor_count += 1
      sent = []
      instructor = class_time.session.user
      _dict = {
        'user': instructor,
        'la_key': LimitedAccessKey.new(instructor),
        'SITE_URL': settings.SITE_URL,
        'session': class_time.session,
        'class_time': class_time,
      }
      send_mail(
        "You're teaching tomorrow at %s!"%class_time.start.strftime("%I:%M"),
        render_to_string("email/teaching_reminder.html",_dict),
        settings.DEFAULT_FROM_EMAIL,
        [instructor.email],
      )
      for enrollment in class_time.session.enrollment_set.all():
        student_count += 1
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
        send_mail(
          "Class tomorrow!",
          render_to_string("email/course_reminder.html",_dict),
          settings.DEFAULT_FROM_EMAIL,
          [user.email],
          )
    print "\n\n\nemailed %s instructors and %s students"%(instructor_count,student_count)
