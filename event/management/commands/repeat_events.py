from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

import datetime,calendar

from event.models import Event,EventOccurrence

def add_month(date):
    if not date:
        return
    year = date.year
    month = date.month + 1
    if month >12:
        year += 1
        month = 1
    return date.replace(year=year,month=month)

def add_month_dow(date):
    if not date:
        return
    monthcalendar = calendar.Calendar(firstweekday=6).monthdayscalendar(date.year,date.month)
    for i,week in enumerate(monthcalendar):
        if date.day in week:
            weekday  = week.index(date.day)
            weeknum = i
            break
    if not monthcalendar[0][weekday]:
        weeknum -= 1
    next_month = add_month(date)
    monthcalendar = calendar.Calendar(firstweekday=6).monthdayscalendar(next_month.year,next_month.month)
    if not monthcalendar[0][weekday]:
        weeknum += 1
    return next_month.replace(day=monthcalendar[weeknum][weekday])

class Command (BaseCommand):
  def handle(self, *args, **options):
      event_set = Event.objects.filter(repeat__isnull=False)
      now = datetime.datetime.now()
      year_from_now = now+datetime.timedelta(365)
      for event in event_set:
          last_occurrence = list(event.eventoccurrence_set.all())[-1]
          while last_occurrence.start < year_from_now:
              if event.repeat == 'weekly':
                  start = last_occurrence.start+datetime.timedelta(7)
                  end = last_occurrence.end + datetime.timedelta(7)
              if event.repeat =='month-dow':
                  start = add_month_dow(last_occurrence.start)
                  end = add_month_dow(last_occurrence.end)
              if event.repeat == 'month-number':
                  start = add_month(last_occurrence.start)
                  end = add_month(last_occurrence.end)
              last_occurrence = EventOccurrence(start=start,end=end,event=event)
              last_occurrence.save()
              print "%s occurrence created on %s"%(event,last_occurrence.end)
