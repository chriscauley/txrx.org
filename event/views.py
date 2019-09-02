from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.template.response import TemplateResponse
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

from .utils import make_ics,ics2response
from .models import Event, EventOccurrence, RSVP, CheckIn, EventRepeat
from tool.models import Criterion, UserCriterion
from course.models import ClassTime
from user.models import is_toolmaster

import datetime, json, arrow, calendar

@staff_member_required
def no_orientation(request):
  users = get_user_model().objects.exclude(level_id=settings.DEFAULT_MEMBERSHIP_LEVEL)
  users = users.exclude(usercriterion__criterion_id=settings.ORIENTATION_CRITERION_ID)
  values = {
    'users': users.distinct().order_by("-date_joined"),
    }
  return TemplateResponse(request,"event/no_orientations.html",values)

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
    events = EventOccurrence.objects.filter(event__hidden=False,**kwargs).select_related("event")
    classtimes = ClassTime.objects.filter(session__course__active=True,session__active=True,**kwargs)
    classtimes = classtimes.select_related("session","session__course")
    week.append((day,sorted(list(events)+list(classtimes),key=lambda s:s.start)))
    if len(week) == 7:
      weeks.append(week)
      week = []
  non_member = True
  if request.user.is_authenticated():
    non_member = request.user.level_id == settings.DEFAULT_MEMBERSHIP_LEVEL
  values = {
    'weeks': weeks,
    'current_date': start,
    'next': datetime.date(year if month!=12 else year+1,month+1 if month!=12 else 1,1),
    'previous': datetime.date(year if month!=1 else year-1,month-1 if month!=1 else 12,1),
    'non_member': non_member,
  }
  return TemplateResponse(request,'event/index.html',values)

#! TODO DEPRACATED 3/2017
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

@cache_page(12*60*60)
def ics(request,module,model_str,pk,fname):
  """Returns an ics file for any `Event` like or `EventOccurrence` like model.
     An `Event` model will add an entry for `Event.all_occurrences()`."""
  model = apps.get_model(module,model_str)
  event = get_object_or_404(model,pk=pk)
  try:
    occurrences = event.all_occurrences.filter(start__gte=timezone.now()-datetime.timedelta(60))
  except AttributeError: # single occurrence
    occurrences = [event]

  calendar_object = make_ics(occurrences,title=event.name)
  return ics2response(calendar_object,fname=fname)

@cache_page(12*60*60)
def all_ics(request,fname):
  occurrences = EventOccurrence.objects.filter(start__gte=timezone.now()-datetime.timedelta(60),event__hidden=False)
  calendar_object = make_ics(occurrences,title="%s Events"%settings.SITE_NAME)
  return ics2response(calendar_object,fname=fname)

@login_required
def rsvp(request):
  occurrence = get_object_or_404(EventOccurrence,id=request.GET['occurrence_id'])
  event = occurrence.event
  if event.access.icon == "members-only" and request.user.level_id == settings.DEFAULT_MEMBERSHIP_LEVEL:
    return JsonResponse({'error': "Only member's are allowed to RSVP for this event"})
  if event.get_user_rsvps(request.user,status="completed"):
    return JsonResponse({'error': "You have been approved by the TXRX tech to work unattended in this area. There is no need to RSVP. You may come in and work during your regular membership times."})
  if not settings.DEBUG and event.orientation_required and not request.user.has_criterion(settings.ORIENTATION_CRITERION_ID):
    orientation_url = Event.objects.get(id=settings.ORIENTATION_EVENT_ID).get_absolute_url()
    a = "<a href='%s'>%s</a>"%(orientation_url,'Click here to RSVP for an orientation.')
    return JsonResponse({'error': "You must attend an orientation before attending this event. %s"%a})
  kwargs = {
    'content_type_id': EventOccurrence._cid,
    'user': request.user,
    'object_id': request.GET['occurrence_id'],
  }
  if request.GET['quantity'] == '0':
    RSVP.objects.filter(**kwargs).delete()
  else:
    rsvp,new = RSVP.objects.get_or_create(**kwargs)
    rsvp.quantity = request.GET['quantity']
    rsvp.save()
  return JsonResponse(occurrence.event.get_user_rsvps(request.user),safe=False)

def detail_json(request,event_pk):
  event = get_object_or_404(Event,pk=event_pk)
  fields = ['id','name','description','hidden','allow_rsvp','owner_ids']
  out = {key:getattr(event,key) for key in fields}
  fields = ['id','name','total_rsvp','start','end','rsvp_cutoff','past']
  if request.user.is_superuser:
    fields.append("total_rsvp")
  os = event.upcoming_occurrences.filter(start__lte=timezone.now()+timezone.timedelta(60))
  out['upcoming_occurrences'] = [{key: getattr(o,key) for key in fields} for o in os]
  return JsonResponse(out)

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

@user_passes_test(is_toolmaster)
def orientations(request,y=None,m=None,d=None):
  criterion_id = settings.ORIENTATION_CRITERION_ID
  criterion = Criterion.objects.get(id=criterion_id)
  if request.POST:
    user = get_user_model().objects.get(id=request.POST['user_id'])
    if request.POST['action'] == 'pass':
      defaults = {'content_object': request.user}
      UserCriterion.active_objects.get_or_create(user=user,criterion=criterion,defaults=defaults)
      messages.success(request,"%s has been oriented."%user)
    else:
      messages.success(request,"%s has been un-oriented."%user)
      UserCriterion.active_objects.filter(user=user,criterion=criterion).delete()
    return HttpResponseRedirect(request.path+"?"+request.GET.urlencode())
  values = {
    'oriented_ids': list(criterion.usercriterion_set.all().values_list('user_id',flat=True)),
  }
  if request.GET.get('q',None):
    users = get_user_model().objects.keyword_search(request.GET['q'],fields="*")
    values['users'] = users[:10]
    if users.count() > 10:
      values['extra_users'] = "Only showing 10/%s users. Please refine your query to see more"%users.count()
    return TemplateResponse(request,'event/orientations.html',values)
  start = datetime.date(int(y),int(m),int(d)) if m and d and y else datetime.date.today()
  end = start + datetime.timedelta(1)
  eventoccurrences = EventOccurrence.objects.filter(event_id=settings.ORIENTATION_EVENT_ID)
  values.update({
    'eventoccurrences': eventoccurrences.filter(start__gte=start,start__lte=end),
    'next_occ': (eventoccurrences.filter(start__gte=end) or [None])[0],
    'prev_occ': (eventoccurrences.filter(start__lte=start).order_by('-start') or [None])[0],
  })
  return TemplateResponse(request,'event/orientations.html',values)

@staff_member_required
def bulk_ajax(request):
  eventrepeat = get_object_or_404(EventRepeat,id=request.GET['eventrepeat_id'])
  if 'day_string' in request.POST:
    st = eventrepeat.start_time
    start = timezone.datetime(*([int(s) for s in request.POST['day_string'].split('-')]+[st.hour,st.minute]))
    if request.POST['action'] == 'remove':
      eventrepeat.month_occurrences.filter(start=start).delete()
    else:
      eventrepeat.eventoccurrence_set.get_or_create(
        start=start,
        end_time=eventrepeat.end_time,
        event=eventrepeat.event
      )
  occurrences = [arrow.get(eo.start).format("YYYY-M-D") for eo in eventrepeat.month_occurrences]
  months = []
  for month in range(5):
    start = arrow.now().replace(day=1,months=month)
    calendar.setfirstweekday(calendar.SUNDAY)
    months.append({
      'name': start.format("MMMM YYYY"),
      'weeks': calendar.monthcalendar(start.year, start.month),
      'number': "%s-%s"%(start.year,start.month)
    })
  return JsonResponse({
    'months': months,
    'occurrences': occurrences,
    'eventrepeat': eventrepeat.as_json,
  })
