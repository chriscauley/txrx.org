from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

from .utils import make_ics,ics2response
from .models import Event, EventOccurrence, RSVP, CheckIn
from tool.models import Criterion, UserCriterion
from course.models import ClassTime

import datetime, json, arrow

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
    kwargs = dict(start__gte=date,start__lte=datetime.timedelta(1)+date)
    events = EventOccurrence.objects.filter(event__hidden=False,**kwargs)
    classtimes = ClassTime.objects.filter(session__course__active=True,session__active=True,**kwargs)
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

def detail(request,event_id,slug=None):
  # NOTE: ze slug does notzing!
  event = get_object_or_404(Event,id=event_id)
  user_rsvps = None
  if request.user.is_authenticated():
    user_rsvps = event.get_user_rsvps(request.user)
  values = {
    'event': event,
    'rsvps_json': json.dumps(user_rsvps)
  }
  return TemplateResponse(request,'event/detail.html',values)

def ics(request,module,model_str,pk,fname):
  """Returns an ics file for any `Event` like or `EventOccurrence` like model.
     An `Event` model will add an entry for `Event.all_occurrences()`."""
  model = apps.get_model(module,model_str)
  event = get_object_or_404(model,pk=pk)
  try:
    occurrences = event.all_occurrences
  except AttributeError: # single occurrence
    occurrences = [event]

  calendar_object = make_ics(occurrences,title=event.name)

  return ics2response(calendar_object,fname=fname)

def all_ics(request,fname):
  occurrences = EventOccurrence.objects.filter(event__hidden=False)

  calendar_object = make_ics(occurrences,title="%s Events"%settings.SITE_NAME)
  return ics2response(calendar_object,fname=fname)

@login_required
def rsvp(request):
  occurrence = get_object_or_404(EventOccurrence,id=request.GET['occurrence_id'])
  kwargs = {
    'content_type_id': EventOccurrence._cid,
    'user': request.user,
    'object_id': request.GET['occurrence_id'],
  }
  if request.GET['quantity'] == 0:
    RSVP.objects.filter(**kwargs).delete()
  else:
    rsvp,new = RSVP.objects.get_or_create(**kwargs)
    rsvp.quantity = request.GET['quantity']
    rsvp.save()
  return HttpResponse(json.dumps(occurrence.event.get_user_rsvps(request.user)))

def detail_json(request,event_pk):
  event = get_object_or_404(Event,pk=event_pk)
  fields = ['name','description','repeat','hidden','allow_rsvp']
  out = {key:getattr(event,key) for key in fields}
  fields = ['id','name','total_rsvp','start','end','rsvp_cutoff']
  if request.user.is_superuser:
    fields.append("total_rsvp")
  os = event.upcoming_occurrences[:10]
  out['upcoming_occurrences'] = [{key: str(getattr(o,key)) for key in fields} for o in os]
  return HttpResponse(json.dumps(out))

@csrf_exempt
def checkin(request):
  User = get_user_model()
  try:
    user = User.objects.get(rfid__number=request.POST['rfid'])
  except User.DoesNotExist:
    response = HttpResponse("Unable to find that user. Try again or contact the staff.")
    response.status_code=401
    return response
  kwargs = {
    'object_id': request.POST.get('object_id',None),
    'checkinpoint_id': request.POST.get('checkinpoint_id',None),
    'content_type_id': request.POST.get('content_type_id',None),
    'user': user,
  }
  # ignore checkins for the same thing with in 10 minutes of each other
  ten_ago = arrow.now().replace(minutes=-10).datetime
  if not CheckIn.objects.filter(datetime__gte=ten_ago,**kwargs):
    CheckIn.objects.create(**kwargs)
  return HttpResponse(json.dumps("%s has been checked in."%user))

def orientations(request,m=None,d=None,y=None):
  if not request.user.is_toolmaster:
    return HttpResponse('not allowed!')
  criterion_id = 15
  criterion = Criterion.objects.get(id=criterion_id)
  if request.POST:
    user = get_user_model().objects.get(id=request.POST['user_id'])
    if request.POST['action'] == 'pass':
      defaults = {'content_object': request.user}
      UserCriterion.objects.get_or_create(user=user,criterion=criterion,defaults=defaults)
      messages.success(request,"%s has been oriented"%user)
    else:
      messages.success(request,"%s has been un-oriented"%user)
      UserCriterion.objects.filter(user=user,criterion=criterion).delete()
    return HttpResponseRedirect(request.path)
  start = datetime.date(y,m,d) if m and d and y else datetime.date.today()
  end = start + datetime.timedelta(1)
  eventoccurrences = EventOccurrence.objects.filter(
    event_id=settings.ORIENTATION_EVENT_ID,
    start__gte=start,
    start__lte=end
  )
  values = {
    'eventoccurrences': eventoccurrences,
    'oriented_ids': list(criterion.usercriterion_set.all().values_list('user_id',flat=True))
  }
  return TemplateResponse(request,'event/orientations.html',values)
