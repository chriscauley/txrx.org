from django.conf import settings
from django.http import HttpResponse
from django.template.defaultfilters import slugify

from course.models import ClassTime
from geo.models import Location
from .models import EventOccurrence

import icalendar, datetime, math
from itertools import groupby
from operator import itemgetter
from pytz import timezone,utc

def make_ics(occurrences=None,title=None):
  """Generate an ics file from an list of occurrences.
     Each occurrence object must have
       obj.description - TextArea (plain text)
       obj.name - CharField
       obj.start - DateTimeField
       obj.end - DatetimeField (Optional)
       obj.get_absolute_url() - a method that returns a url without a domain
     """
  tz = timezone(settings.TIME_ZONE)

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
    start_dt = start_dt.astimezone(utc)

    vevent['uid'] = '%s%d'%(slugify(settings.SITE_NAME),occ.id)
    vevent.add('dtstamp', start_dt)
    vevent.add('dtstart', start_dt)
    if occ.end:
      end_dt = tz.localize(occ.end)
      end_dt = end_dt.astimezone(utc)
      vevent.add('dtend', end_dt)

    vevent.add('summary', occ.name)
    vevent.add('url', '%s%s'%(settings.SITE_URL, occ.get_absolute_url()))
    vevent.add('class', 'PUBLIC')
    vevent.add('x-microsoft-cdo-importance', '1')
    vevent.add('priority', '5')
    vevent.add('description', occ.description)
    vevent.add('location', str(occ.get_location()))

    calObj.add_component(vevent)

  return calObj

def ics2response(calendar_object,fname):
  icalstream = calendar_object.to_ical().replace('TZID=UTC;', '')

  response = HttpResponse(icalstream, mimetype='text/calendar')

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
  return [start+datetime.timedelta(0,block_size*i) for i in range(blocks+1)]

def get_room_conflicts(base_occurrence=None):
  block_size = 60*30 #seconds per half hour
  if base_occurrence:
    start_time = base_occurrence.start-datetime.timedelta(0,block_size)
    end_time = base_occurrence.end+datetime.timedelta(0,block_size)
    location = base_occurrence.location
    class_times = ClassTime.objects.filter(start__gte=start_time,start__lte=end_time,
                                           session__section__no_conflict=False,
                                           session__section__location=location)
    occurrences = EventOccurrence.objects.filter(start__gte=start_time,event__no_conflict=False,
                                                 event__location=location)
    locations = [base_occurrence.location]
  else:
    start_time = datetime.datetime.now()-datetime.timedelta(0,block_size)
    end_time = datetime.datetime.now()+datetime.timedelta(60)
    class_times = ClassTime.objects.filter(start__gte=start_time,start__lte=end_time,
                                           session__section__no_conflict=False)
    occurrences = EventOccurrence.objects.filter(start__gte=start_time,event__no_conflict=False)
    locations = Location.objects.all()
  schedule = {location:{} for location in locations}
  event_tuples = []

  # combine events and classes because they have similar enough APIs to treat them the same 
  for class_time in class_times:
    event_tuples.append((class_time,class_time.session.section.location))
  for occurrence in occurrences:
    event_tuples.append((occurrence, occurrence.get_location()))

  # iterate over 30 minute chunks and group chunks by time and location
  for event,location in event_tuples:
    for time in iter_times(event.start,event.end):
      schedule[location][time] = schedule[location].get(time,[])
      schedule[location][time].append(event)

  #for k,v in sorted(schedule.values()[0].items()):
  #  if len(v) > 1:
  #    print k,'\t',v

  # remove all slots with only one for fewer events in a given room
  room_conflicts = {}
  for location,event_slots in schedule.items():
    room_conflicts[location] = [(dt,events) for dt,events in event_slots.items() if events and len(events)>1]

  # re-group the 30 minute chunks by consecutive slots in a given room
  room_conflicts = [r for r in room_conflicts.items() if r[1]]
  out = []
  for location,conflicts in room_conflicts:
    reshuffled_conflicts = []
    location_conflicts = []
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
      location_conflicts.append((times,events))
    out.append((location,location_conflicts))
  return out
