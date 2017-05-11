#stupid requests ssl error
import warnings;warnings.showwarning = lambda *x: None

from django.conf import settings
from django.core import mail
from django.db import IntegrityError

from course.models import Course, Session, ClassTime
from tool.models import Criterion
from event.models import Event, EventOccurrence
from lablackey.geo.models import Room, Location, City
from lablackey.tests import check_subjects
from membership.models import Level

from drop.test_utils import DropTestCase

import datetime, decimal, six, arrow, random

class TXRXTestCase(DropTestCase):
  fixture_apps = [".dev/lablackey/geo/","tool"]
  def setUp(self,*args,**kwargs):
    super(TXRXTestCase,self).setUp(*args,**kwargs)
    self._setup_membership()
    self._setup_course()
  def _setup_course(self):
    tomorrow = arrow.now().replace(days=1,hour=13,minute=00).datetime
    next_day = arrow.now().replace(days=2,hour=13,minute=00).datetime
    end = "14:00"
    kwargs = dict(
      active=True,
      no_conflict=True,
      room_id=1
    )
  
    self.course1 = Course.objects.create(name="course45",fee=45,**kwargs)
    self.course2 = Course.objects.create(name="course50",fee=50,**kwargs)

    self.teacher = self.new_user()
    self.student1 = self.new_user()
    self.student2 = self.new_user()
    # fee = 45 because it tests that discounts are including fractional dollars
    # Session 1 has class tomorrow and the next day from 1-2pm
    self.session1 = Session.objects.create(course=self.course1,user=self.teacher)
    self.session1.save()
    ClassTime.objects.create(session=self.session1,start=tomorrow,end_time=end)
    ClassTime.objects.create(session=self.session1,start=next_day,end_time=end)
    self.session1 = Session.objects.get(pk=self.session1.pk)

    # Session 2 has class day after tomorrow at the same time as session 1
    self.session2 = Session.objects.create(course=self.course2,user=self.teacher)
    ClassTime.objects.create(session=self.session2,start=tomorrow.replace(hour=18),end_time="19:00")
    self.session2.save()

    # A second session for course 2, the next week
    self.session22 = Session.objects.create(course=self.course2,user=self.teacher)
    ClassTime.objects.create(session=self.session22,start=tomorrow.replace(hour=18)+datetime.timedelta(7),end_time="19:00")
    self.session22.save()

    # # conflict_session1 is the same time as session1. currently unused
    # self.conflict_session1 = Session.objects.create(
    #   course=Course.objects.filter(active=True,fee__gt=0).order_by("?")[0],
    #   user_id=1
    # )
    # ClassTime.objects.create(session=self.conflict_session1,start=next_day,end_time=end)

  def _setup_membership(self):
    try:
      self.level0 = Level.objects.get(id=settings.DEFAULT_MEMBERSHIP_LEVEL)
    except Level.DoesNotExist:
      self.level0 = Level.objects.create(id=settings.DEFAULT_MEMBERSHIP_LEVEL,name='foo',order=1)
    self.level10 = Level.objects.get_or_create(name="discounted",discount_percentage=10,order=999,id=10000)[0]
    for level in Level.objects.all():
      p = int(random.random()*100)
      level.product_set.get_or_create(name="monthly %s"%level,unit_price=p,months=1,active=True)
      level.product_set.get_or_create(name="yearly %s"%level,unit_price=p*11,months=12,active=True)

class ManagementCommands(DropTestCase):
  def setUp(self):
    self.now = datetime.datetime.now()
    self.in_an_hour = (self.now + datetime.timedelta(0,60*60)).time()
    self.tomorrow = self.now + datetime.timedelta(1)

  def test_repeat_events(self):
    Event.objects.filter(name="monkey").delete()
    e = Event.objects.create(name="monkey",repeat="month-number")
    eo = EventOccurrence.objects.create(start=self.tomorrow,end_time=self.in_an_hour,event=e)
    self.call_command("repeat_events")
    self.assertEqual(e.eventoccurrence_set.count(),5)
    subjects = [m.subject for m in mail.outbox]
    self.assertTrue(check_subjects([]))

  def test_evaluation_reminder(self):
    self.call_command("evaluation_reminder")
  def test_recalculate_subscriptions(self):
    self.call_command("recalculate_subscriptions")

  # done in course.tests
  #def test_course_reminder(self):
  #  self.call_command("course_reminder")

  def test_notify_course(self):
    self.call_command("notify_course")
  def test_reset_classes(self):
    self.call_command("reset_classes")
