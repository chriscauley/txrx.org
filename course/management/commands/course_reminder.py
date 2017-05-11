from django.conf import settings
from django.core.mail import send_mail,mail_admins
from django.core.management.base import BaseCommand
from django.template.defaultfilters import date
from django.template.loader import render_to_string
from django.utils import timezone

from course.models import ClassTime
from event.models import EventOccurrence
from membership.models import LimitedAccessKey
from notify.models import Notification

import arrow

class Command(BaseCommand):
  def handle(self, *args, **options):
    tomorrow = arrow.utcnow().replace(hour=6,days=1).datetime
    next_day = arrow.utcnow().replace(hour=6,days=2).datetime
    classtimes = ClassTime.objects.filter(start__gte=tomorrow,start__lte=next_day,emailed__isnull=True)
    classtimes = classtimes.exclude(session__course__active=False).exclude(session__active=False).distinct()
    if not classtimes:
      return
    if options.get("verbosity") > 0:
      print "showing classes from %s to %s"%(tomorrow,next_day)
      print "reminding %s class times"%len(classtimes)
    instructor_count = 0
    student_count = 0
    sent = []
    for classtime in classtimes:
      instructor_count += 1
      instructor = classtime.session.user
      user_messages = []

      day_s = date(classtime.start,"P [n/j]")
      kwargs = {
        'url': classtime.session.get_absolute_url(),
        'target_type': "course.classtime",
        'target_id':classtime.id,
        'expires': classtime.end
      }

      _s = "%s at %s"%(classtime.session.course.get_short_name(),day_s)
      Notification.objects.create(
        user=instructor,
        message="You're teaching %s"%_s,
        relationship="teaching_reminder",
        **kwargs
      )
      for enrollment in classtime.session.enrollment_set.all():
        student_count += 1
        Notification.objects.create(
          user=enrollment.user,
          message="You're taking %s"%_s,
          relationship="course_reminder",
          **kwargs
        )
      classtime.emailed = timezone.now()
      classtime.save()
    if options.get("verbosity") > 0:
      print "\n\n\nemailed %s instructors and %s students"%(instructor_count,student_count)
