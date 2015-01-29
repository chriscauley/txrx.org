from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from course.models import ClassTime
from event.models import EventOccurrence
from geo.models import Location, Room
from .forms import RoomFormSet

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

@staff_member_required
def room_picker(request,pk):
  location = Location.objects.get(pk=pk)
  formset = RoomFormSet(
    request.POST or None,
    queryset=location.room_set.all()
  )
  if formset.is_valid():
    formset.save()
    messages.success(request,"Forms Saved")
    return HttpResponseRedirect(request.path)
  elif request.method == "POST":
    messages.error(request,"Something seems to be wrong, check all fields and try again.")
  values = {
    'location': location,
    'formset': formset,
  }
  return TemplateResponse(request,'geo/room_picker.html',values)

@staff_member_required
def dxfviewer(request,pk=None):
  today = datetime.datetime.now().replace(hour=0,minute=0)
  tomorrow = today + datetime.timedelta(1)
  events = EventOccurrence.objects.filter(start__gte=today,start__lte=tomorrow)
  classtimes = ClassTime.objects.filter(start__gte=today,start__lte=tomorrow)
  events = list(events)+list(classtimes)
  event_dict = {}
  for event in events:
    if not event.start in event_dict:
      event_dict[event.start] = []
    event_dict[event.start].append(event)
  if not pk:
    pk = 1
  values = {
    'location': Location.objects.get(pk=pk),
    'event_tuples': sorted(event_dict.items(),key=lambda t:t[0]),
  }
  return TemplateResponse(request,'dxf.html',values)
