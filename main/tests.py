from django.test import TestCase
from django.core.management import call_command
from django.core import mail

from lablackey.tests import check_subjects
from event.models import Event, EventOccurrence

import datetime

class ManagementCommands(TestCase):
  def setUp(self):
    self.now = datetime.datetime.now()
    self.in_an_hour = (self.now + datetime.timedelta(0,60*60)).time()
    self.tomorrow = self.now + datetime.timedelta(1)

  def test_repeat_events(self):
    Event.objects.filter(name="monkey").delete()
    e = Event.objects.create(name="monkey",repeat="month-number")
    eo = EventOccurrence.objects.create(start=self.tomorrow,end_time=self.in_an_hour,event=e)
    call_command("repeat_events")
    self.assertEqual(e.eventoccurrence_set.count(),5)
    subjects = [m.subject for m in mail.outbox]
    self.assertTrue(check_subjects([]))

  def test_evaluation_reminder(self):
    call_command("evaluation_reminder")
  def test_recalculate_subscriptions(self):
    call_command("recalculate_subscriptions")

  # done in course.tests
  #def test_course_reminder(self):
  #  call_command("course_reminder")

  def test_notify_course(self):
    call_command("notify_course")
  def test_reset_classes(self):
    call_command("reset_classes")
