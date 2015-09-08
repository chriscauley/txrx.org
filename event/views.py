from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.template.defaultfilters import slugify

from django.apps import apps
get_model = apps.get_model

from .utils import make_ics,ics2response
from .models import Event, EventOccurrence
from course.models import ClassTime

import datetime

def index(request,daystring=None):
  start = datetime.date.today()
  if daystring:
    start = datetime.datetime.strptime(daystring,'%Y-%m-%d').date()
    dt = start - datetime.date.today()
    if dt.days < -770 or dt.days > 365:
      print "DDoS: %s || %s"%(request.META['HTTP_USER_AGENT'],request.META['REMOTE_ADDR'])
      raise Http404("You have selected a date too far in the future or past.")
  end = start+datetime.timedelta(7)
  year = start.year
  month = start.month
  first = datetime.date(year,month,1)
  weeks = []
  week = []
  if first.isoweekday() != 7:
    week = [('',[])]*first.isoweekday()
  day = 0
  while True:
    day += 1
    try:
      date = datetime.date(year,month,day)
    except ValueError:
      if week:
        weeks.append(week)
      break
    events = EventOccurrence.objects.filter(start__gte=date,start__lte=datetime.timedelta(1)+date)
    classtimes = ClassTime.objects.filter(start__gte=date,start__lte=datetime.timedelta(1)+date,
                                          session__course__active=True,session__active=True)
    week.append((day,sorted(list(events)+list(classtimes),key=lambda s:s.start)))
    if len(week) == 7:
      weeks.append(week)
      week = []
  values = {
    'weeks': weeks,
    'current_date': start,
    'next': datetime.date(year if month!=12 else year+1,month+1 if month!=12 else 1,1),
    'previous': datetime.date(year if month!=1 else year-1,month-1 if month!=1 else 12,1),
    }
  return TemplateResponse(request,'event/index.html',values)

def occurrence_detail(request,occurrence_id,slug=None):
  # NOTE: the above slug does nothing, it is only for prettier urls
  occurrence = get_object_or_404(EventOccurrence,pk=occurrence_id)
  values = {
    'occurrence': occurrence,
    }
  return TemplateResponse(request,'event/occurrence_detail.html',values)

# depracated 9/2014
"""
def repeat_event(request,period,event_id):
  event = get_object_or_404(Event,pk=event_id)
  occurrences = event.upcoming_occurrences
  start = occurrences[0].start
  end = occurrences[0].end
  occurrences.delete()
  if period == 'weekly':
    days = 7
    message = "This event has been repeated weekly for a year."
  else:
    days = 30
    message = "This event has been repeated every thirty days for a year. Please check for accuracy."
  count = 0
  while count < 365:
    td = datetime.timedelta(count)
    e = EventOccurrence(
      event=event,
      start=start+td,
      )
    if end:
      e.end=end+td
    e.save()
    count += days
  messages.success(request,"All upcoming occurrences have been deleted.")
  messages.success(request,message)
  return HttpResponseRedirect(request.META['HTTP_REFERER'])
"""

def ics(request,module,model_str,pk,fname):
  """Returns an ics file for any `Event` like or `EventOccurrence` like model.
     An `Event` model will add an entry for `Event.all_occurrences()`.
     """
  model = get_model(module,model_str)
  event = get_object_or_404(model,pk=pk)
  try:
    occurrences = event.all_occurrences
  except AttributeError: # single occurrence
    occurrences = [event]

  calendar_object = make_ics(occurrences,title=event.name)

  return ics2response(calendar_object,fname=fname)

def all_ics(request,fname):
  occurrences = EventOccurrence.objects.all()

  calendar_object = make_ics(occurrences,title="TX/RX Labs Events")
  return ics2response(calendar_object,fname=fname)
