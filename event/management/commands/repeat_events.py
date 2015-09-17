from django.core.management.base import BaseCommand
from django.core.mail import send_mail,mail_admins
from django.conf import settings

import datetime,calendar, traceback

from event.models import Event,EventOccurrence
from lablackey.mail import print_to_mail

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
  try:
    return next_month.replace(day=monthcalendar[weeknum][weekday])
  except IndexError: # last week of month
    return next_month.replace(day=monthcalendar[weeknum-1][weekday])

class Command (BaseCommand):
  @print_to_mail(subject="[LOG] Repeating Events")
  def handle(self, *args, **options):
    success = []
    errors = []
    event_set = Event.objects.filter(repeat__isnull=False)
    now = datetime.datetime.now()
    year_from_now = now+datetime.timedelta(120) #actually 4 months!
    for event in event_set:
      try:
        last_occurrence = list(event.eventoccurrence_set.all())[-1]
        while last_occurrence.start < year_from_now:
          end_time = last_occurrence.end_time
          occurrences = []
          if 'weekly' in event.repeat:
            _map = {'weekly':2,'biweekly':3,'triweekly':4}
            for i in range(1,_map[event.repeat]):
              last_occurrence = list(event.eventoccurrence_set.all())[-i]
              start = last_occurrence.start+datetime.timedelta(7)
              occurrences.append({'start':start,'end_time':end_time})
          if event.repeat =='month-dow':
            start = add_month_dow(last_occurrence.start)
            occurrences.append({'start':start,'end_time':end_time})
          if event.repeat == 'month-number':
            start = add_month(last_occurrence.start)
            occurrences.append({'start':start,'end_time':end_time})
          for occurrence in occurrences:
            last_occurrence = EventOccurrence(event=event,**occurrence)
            last_occurrence.save()
            success.append("%s occurrence created on %s"%(event,last_occurrence.start))
      except Exception, err:
        if settings.DEBUG:
          raise
        errors.append("%s error: \n%s"%(event,traceback.format_exc()))
    if errors:
      print "event errors\n--------%s\n\n"%'\n'.join(errors)
    if success:
      print "event sucess\n--------%s\n\n"%'\n'.join(sucess)
