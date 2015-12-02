from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse

from course.models import ClassTime
from event.models import EventOccurrence
from geo.models import Location, Room, RoomGroup

import datetime, math, json

def iter_times(start,end):
  kwargs = dict(second=0,microsecond=0)
  start = start.replace(minute=start.minute-start.minute%30,**kwargs) # round back to the nearest half hour
  td = end - start
  block_size = 60*30 #seconds per half hour
  blocks = int(math.ceil(td.total_seconds()/(block_size))) #half hours that this runs
  return [start+datetime.timedelta(0,block_size*i) for i in range(blocks)]

def events_json(request):
  today = datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
  if 'YMD' in request.GET:
    today = arrow.get(request.GET['YMD'],"YYYY-MM-DD").datetime
  tomorrow = today + datetime.timedelta(1)
  events = EventOccurrence.objects.filter(event__hidden=False,start__gte=today,start__lte=tomorrow)
  classtimes = ClassTime.objects.filter(start__gte=today,start__lte=tomorrow)
  events = list(events)+list(classtimes)
  event_dict = {}
  for event in events:
    if not event.start in event_dict:
      event_dict[event.start] = []
    event_dict[event.start].append(event)
  event_tuples = sorted(event_dict.items(),key=lambda t:t[0])
  out = [{
    'datetime': str(t[0]),
    'events': [e.as_json for e in t[1]]
  } for t in event_tuples]
  return HttpResponse(json.dumps(out))

def locations_json(request):
  # return locations for specified pks or return all locations
  locations = Location.objects.all()
  if 'pks' in request.GET:
    locations = locations.filter(pk__in=request.GET.get('pks',None).split(','))
  return HttpResponse(json.dumps({
    'locations': { l.id: l.as_json for l in locations },
    'rooms': { r.id: r.as_json for r in Room.objects.all() },
    'roomgroups': { g.id: g.as_json for g in RoomGroup.objects.all() }
  }))

def dxfviewer(request,pk=None):
  if not pk:
    pk = 1
  values = {
    'location': Location.objects.get(pk=pk),
    'roomgroups': RoomGroup.objects.all(),
  }
  return TemplateResponse(request,'dxf.html',values)
