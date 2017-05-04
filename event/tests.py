from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from event.models import EventRepeat, Event, Access, EventOccurrence

import calendar, arrow, datetime

class EventRepeatTestCase(TestCase):
  def setUp(self):
    access = Access.objects.create(name='test')
    self.event = Event.objects.create(access=access)
    self.event2 = Event.objects.create(access=access)
  def test_eventrepeat_generate(self):
    #Every Friday in year
    year = 2017
    _re = EventRepeat.objects.create(
      event=self.event,
      start_time=datetime.datetime(2017,1,1,12).time(),
      end_time=datetime.datetime(2017,1,1,13).time(),
      repeat_flavor='weekly',
      first_date=datetime.date(year,1,6) # Jan 1, 2017 is a friday
    )
    eventrepeat = EventRepeat.objects.get(id=_re.id)
    eventrepeat.generate(start_datetime=datetime.datetime(year,1,1),end_date=datetime.datetime(year,12,31))
    occurrences = eventrepeat.eventoccurrence_set.all()
    for occurrence in occurrences:
      self.assertEqual(occurrence.start.year,year)
    eventrepeat.generate(start_datetime=datetime.datetime(year+1,1,1),end_date=datetime.datetime(year+1,1,31))
    for occurrence in occurrences:
      self.assertEqual(occurrence.start.isoweekday(),5)
      self.assertEqual(occurrence.start.hour, 12)
      self.assertEqual(occurrence.end.hour, 13)
    for occurrence in occurrences.filter(start__gte="%s-1-1"%(year+1)):
      self.assertEqual(occurrence.start.year,year+1)
      self.assertEqual(occurrence.start.month,1)

    # check to make sure last day is end of january (25 is latest possible friday)
    self.assertTrue(occurrence.start.day > 24)

    #create 2x monthly repeat on first and third fridays (similar to open house at TXRX)
    _re = EventRepeat.objects.create(
      event=self.event2,
      start_time=datetime.datetime(2017,1,1,19).time(),
      end_time=datetime.datetime(2017,1,1,21).time(),
      repeat_flavor='start-month',
      first_date=datetime.date(2017,2,17) #two weeks after first friday
    )
    eventrepeat = EventRepeat.objects.get(id=_re.id)
    eventrepeat.generate(start_datetime=datetime.datetime(year,1,1),end_date=datetime.datetime(year,12,31))
    occurrences = eventrepeat.eventoccurrence_set.all()
    self.assertEqual(occurrences.count(),12)

    _re = EventRepeat.objects.create(
      event=self.event2,
      start_time=datetime.datetime(2017,1,1,19).time(),
      end_time=datetime.datetime(2017,1,1,21).time(),
      repeat_flavor='start-month',
      first_date=datetime.date(2017,3,3) #two weeks after first friday
    )
    eventrepeat = EventRepeat.objects.get(id=_re.id)
    eventrepeat.generate(start_datetime=datetime.datetime(year,1,1),end_date=datetime.datetime(year,12,31))
    occurrences = eventrepeat.eventoccurrence_set.all()
    self.assertEqual(occurrences.count(),12)
