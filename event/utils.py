from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.template.defaultfilters import slugify
from django.utils import timezone

from course.models import ClassTime
from lablackey.geo.models import Room
from .models import EventOccurrence, OccurrenceModel # Occurrence model used to make non-db objects

import icalendar, datetime, math, arrow, pytz
from collections import defaultdict
from itertools import groupby
from operator import itemgetter

def make_ics(occurrences=None,title=None):
  """Generate an ics file from an list of occurrences.
     Each occurrence object must have
       obj.description - TextArea (plain text)
       obj.name - CharField
       obj.start - DateTimeField
       obj.end - DatetimeField (Optional)
       obj.get_absolute_url() - a method that returns a url without a domain
     """
  tz = pytz.timezone(settings.TIME_ZONE)

  name = "%s @ %s"%(title,settings.SITE_NAME)
  calObj = icalendar.Calendar()
  calObj.add('method', 'PUBLISH')  # IE/Outlook needs this
  calObj.add('version','2.0')
  calObj.add('prodid', '-//%s calendar product//mxm.dk//'%settings.SITE_NAME)

  calObj.add('x-wr-calname', name)
  calObj.add('name', name)

  for occ in occurrences:
    vevent = icalendar.Event()
    start_dt = tz.localize(occ.start)
    start_dt = start_dt.astimezone(pytz.utc)

    vevent['uid'] = '%s%d'%(slugify(settings.SITE_NAME),occ.id)
    vevent.add('dtstamp', start_dt)
    vevent.add('dtstart', start_dt)
    if occ.end:
      end_dt = tz.localize(occ.end)
      end_dt = end_dt.astimezone(pytz.utc)
      vevent.add('dtend', end_dt)

    vevent.add('summary', occ.name)
    vevent.add('url', '%s%s'%(settings.SITE_URL, occ.get_absolute_url()))
    vevent.add('class', 'PUBLIC')
    vevent.add('x-microsoft-cdo-importance', '1')
    vevent.add('priority', '5')
    vevent.add('description', occ.description)
    vevent.add('room', str(occ.get_room()))

    calObj.add_component(vevent)

  return calObj

def ics2response(calendar_object,fname):
  icalstream = calendar_object.to_ical().replace('TZID=UTC;', '')

  response = HttpResponse(icalstream, content_type='text/calendar')

  response['Filename'] = '%s.ics'%fname
  response['Content-Disposition'] = 'attachment; filename=%s.ics'%fname
  response['Content-Length'] = len(icalstream)

  return response

def iter_times(start,end):
  kwargs = dict(second=0,microsecond=0)
  # round back to the nearest half hour
  start = start.replace(minute=start.minute-start.minute%30,**kwargs)
  td = end - start
  block_size = 60*30 #seconds per half hour
  blocks = int(math.ceil(td.total_seconds()/(block_size))) #half hours that this runs
  return [start+datetime.timedelta(0,block_size*i) for i in range(blocks)]

def get_person_conflicts(target_user_id=None,base_occurrence=None):
  """
  Finds users who are an instructor or an "event owner" for concurrent classes/events.
  Returns a list of conflicts of the form:
  [user,start_datetime,end_datetime,conflicting_events]
  """
  if isinstance(target_user_id,get_user_model()):
    target_user_id = target_user_id.id

  # break events durations into "blocks" to look for overlaps
  # a block is actually just a datetime, but it implies a range, [sometime,sometime+timedelta(block_size)
  # so an event from 12:15 to 15:00 would yield 12:00, 12:30, 13:00... 14:30
  block_minutes = 30
  block_size = 60*block_minutes #seconds per half hour
  user_timess = {}
  start_time = timezone.now().replace(minute=0)
  end_time = timezone.now() + datetime.timedelta(60)
  if base_occurrence:
    start_time = base_occurrence.start
    end_time = base_occurrence.end
  user_occurrences = defaultdict(lambda: defaultdict(list)) # { user_id: { block_datetime: [occurrences] } }

  # Anything inheriting from OccurrenceModels should have the necessary API to run through this loop
  models = [ClassTime,EventOccurrence]
  occurrences = []
  for model in models:
    occurrences += list(model.objects.filter(start__gte=start_time,start__lte=end_time))
  for occ in occurrences:
    for user_id in occ.get_owner_ids():
      if user_id in [1,1273]:
        continue
      if target_user_id and user_id != target_user_id:
        continue
      _block = occ.start
      if _block > occ.end:
        mail_admins("bad times on an occurrence","checkout: %s (#%s)"%(occ,occ.id))
      # this rounds down to the nearest block, eg 17:34:5.938475  > 17:30:00
      _block = _block.replace(minute=_block.minute-_block.minute%block_minutes,second=0,microsecond=0)
      while _block <= occ.end:
        user_occurrences[user_id][_block].append(occ)
        _block += datetime.timedelta(0,block_size) # move to next block
  conflicts = []
  for user_id,block_dict in user_occurrences.items():
    block_events = sorted({ k:v for k,v in block_dict.items() if len(v) > 1 }.items())
    for events,group in groupby(block_events,lambda k:sorted(k[1])):
      times = [g[0] for g in group]
      conflicts.append((get_user_model().objects.get(id=user_id),min(times),max(times),events))
  return conflicts

def get_room_conflicts(base_occurrence=None):
  block_size = 60*30 #seconds per half hour
  if base_occurrence:
    # only look only during the time of this class accorss all rooms
    start_time = base_occurrence.start-datetime.timedelta(0,block_size)
    start_time = start_time.replace(hour=0,minute=0)
    end_time = start_time+datetime.timedelta(1)
    room = base_occurrence.room
    _class_times = ClassTime.objects.filter(start__gte=start_time,start__lte=end_time,
                                            session__course__no_conflict=False)
    occurrences = EventOccurrence.objects.filter(start__gte=start_time,start__lte=end_time,event__no_conflict=False)
  else:
    # Look accross the next 60 days in all rooms
    start_time = datetime.datetime.now()-datetime.timedelta(0,block_size)
    end_time = datetime.datetime.now()+datetime.timedelta(90)
    _class_times = ClassTime.objects.filter(start__gte=start_time,start__lte=end_time,
                                            session__course__no_conflict=False)
    occurrences = EventOccurrence.objects.filter(start__gte=start_time,start__lte=end_time,event__no_conflict=False)
  rooms = Room.objects.all()
  class_times = []
  for ct in set(_class_times):
    class_times += ct.build_class_times()
  schedule = {room:{} for room in rooms}

  # combine events and classes because they have similar enough APIs to treat them the same 
  for occurrence in (list(occurrences)+class_times):
    room = occurrence.get_room()
    if not room in rooms:
      continue
    for time in iter_times(occurrence.start,occurrence.end):
      schedule[room][time] = schedule[room].get(time,[])
      schedule[room][time].append(occurrence)

  # remove all slots with only one for fewer events in a given room
  room_conflicts = {}
  for room,event_slots in schedule.items():
    room_conflicts[room] = [(dt,events) for dt,events in event_slots.items() if events and len(events)>1]

  # re-group the 30 minute chunks by consecutive slots in a given room
  room_conflicts = [r for r in room_conflicts.items() if r[1]]
  out = []
  for room,conflicts in room_conflicts:
    has_base_occurrence = not base_occurrence
    reshuffled_conflicts = []
    room_conflicts = []
    conflicts.sort(key=lambda i:i[0])
    func = lambda (i,(dt,events)): dt-datetime.timedelta(0,i*60*30)
    for k,g in groupby(enumerate(conflicts),key=func):
      reshuffled_conflicts.append(map(itemgetter(1), g))
    for conflict_spots in reshuffled_conflicts:
      times,_event_mess = zip(*conflict_spots)
      times = [times[0], times[-1]]
      if (times[-1] - times[0]).total_seconds() < 30*60:
        continue
      events = []
      for e in _event_mess:
        events += e
      events = list(set(events))
      if not has_base_occurrence and base_occurrence in events:
        has_base_occurrence = True
      room_conflicts.append((times,events))
    if room_conflicts and has_base_occurrence:
      out.append((room,room_conflicts))
  return out

def _conflicts(a,b):
  return not (a.ends < b.starts or b.ends < a.starts)
