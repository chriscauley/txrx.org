from django.test import TestCase
from django.utils import timezone

from event.models import RepeatEvent, Event

import calendar, arrow, datetime

class RepeatEventTestCase(TestCase):
  def setUp(self):
    self.event = Event.objects.create()
  def test_repeatevent_generate(self):
    #Every Friday in year
    year = 2017
    _re = RepeatEvent.objects.create(
      event=self.event,
      start='12:00',
      end='13:00',
      repeat_flavor='weekly',
      first_date=datetime.date(year,1,6)
    )
    repeatevent = RepeatEvent.objects.get(id=_re.id)
    repeatevent.generate(start_datetime=datetime.datetime(year,1,1),end_date=datetime.datetime(year,12,31))
    occurrences = repeatevent.eventoccurrence_set.all()
    for occurrence in occurrences:
      self.assertEqual(occurrence.start.year,year)
    repeatevent.generate(start_datetime=datetime.datetime(year+1,1,1),end_date=datetime.datetime(year+1,1,31))
    for occurrence in occurrences:
      self.assertEqual(occurrence.start.isoweekday(),5)
      self.assertEqual(occurrence.start.hour, 12)
      self.assertEqual(occurrence.end.hour, 13)
    for occurrence in occurrences.filter(start__gte="%s-1-1"%(year+1)):
      self.assertEqual(occurrence.start.year,year+1)
      self.assertEqual(occurrence.start.month,1)

    # check to make sure last day is end of january
    self.assertTrue(occurrence
