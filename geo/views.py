from django.contrib.admin.views.decorators import staff_member_required
from django.template.response import TemplateResponse

from course.models import ClassTime
from event.models import EventOccurrence
from geo.models import Location, Room

import datetime, math
from itertools import groupby
from operator import itemgetter

def iter_times(start,end):
  kwargs = dict(second=0,microsecond=0)
  start = start.replace(minute=start.minute-start.minute%30,**kwargs) # round back to the nearest half hour
  td = end - start
  block_size = 60*30 #seconds per half hour
  blocks = int(math.ceil(td.total_seconds()/(block_size))) #half hours that this runs
  return [start+datetime.timedelta(0,block_size*i) for i in range(blocks)]

def get_room_conflicts(td=0):
  start_time = datetime.datetime.now()-datetime.timedelta(td)
  end_time = datetime.datetime.now()+datetime.timedelta(60-td)
  class_times = ClassTime.objects.filter(start__gte=start_time,start__lte=end_time,session__section__no_conflict=False)
  occurrences = EventOccurrence.objects.filter(start__gte=start_time,event__no_conflict=False)
  rooms = Room.objects.all()
  schedule = {room:{} for room in rooms}
  event_tuples = []

  # combine events and classes because they have similar enough APIs to treat them the same
  for class_time in class_times:
    event_tuples.append((class_time,class_time.session.section.room))
  for occurrence in occurrences:
    event_tuples.append((occurrence, occurrence.get_room()))

  # iterate over 30 minute chunks and group chunks by time and room
  for event,room in event_tuples:
    for time in iter_times(event.start,event.end):
      schedule[room][time] = schedule[room].get(time,[])
      schedule[room][time].append(event)

  # remove all slots with only one for fewer events in a given room
  room_conflicts = {}
  for room,event_slots in schedule.items():
    room_conflicts[room] = []
    for dt,events in event_slots.items():
      if not events or len(events) == 1:
        continue
      room_conflicts[room].append((dt,events))

  # re-group the 30 minute chunks by consecutive slots in a given room
  room_conflicts = [r for r in room_conflicts.items() if r[1]]
  out = []
  for room,conflicts in room_conflicts:
    reshuffled_conflicts = []
    room_conflicts = []
    conflicts.sort(key=lambda i:i[0])
    func = lambda (i,(dt,events)): dt-datetime.timedelta(0,i*60*30)
    for k,g in groupby(enumerate(conflicts),key=func):
      reshuffled_conflicts.append(map(itemgetter(1), g))
    for conflict_spots in reshuffled_conflicts:
      times,_event_mess = zip(*conflict_spots)
      times = [times[0], times[-1]]
      events = []
      for e in _event_mess:
        events += e
      events = list(set(events))
      room_conflicts.append((times,events))
    out.append((room,room_conflicts))
  return out

@staff_member_required
def conflicts(request):
  values = {
    'room_conflicts': get_room_conflicts()
  }
  return TemplateResponse(request,"geo/conflicts.html",values)
