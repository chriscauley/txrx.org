from django.template.response import TemplateResponse

from course.models import ClassTime
from event.models import EventOccurrence
from geo.models import Location

import datetime, math

def iter_times(start,end):
  td = end - start
  block_size = 60*30 #seconds per half hour
  blocks = int(math.ceil(td.total_seconds()/(block_size))) #half hours that this runs
  return [start+datetime.timedelta(0,block_size*i) for i in range(blocks)]

def get_room_conflicts(td=0):
  now = datetime.datetime.now()-datetime.timedelta(td)
  two_months = datetime.datetime.now()+datetime.timedelta(60-td)
  class_times = ClassTime.objects.filter(start__gte=now,start__lte=two_months)
  occurrences = EventOccurrence.objects.filter(start__gte=now)
  locations = Location.objects.all()
  schedule = {location:{} for location in locations}
  event_tuples = []
  for class_time in class_times:
    event_tuples.append((class_time,class_time.session.section.location))
  for occurrence in occurrences:
    event_tuples.append((occurrence, occurrence.get_location()))
  for event,location in event_tuples:
    for time in iter_times(event.start,event.end):
      schedule[location][time] = schedule[location].get('time',[])
      schedule[location][time].append(event)
  for location,event_slots in schedule.items():
    for dt,events in event_slots.items():
      if not events or len(events) == 1:
        continue
      print location
      print events
      exit()
