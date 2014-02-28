from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import QueryDict, Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from ..models import Course, Section, Term, Subject, Session, Enrollment, ClassTime
from ..forms import EmailInstructorForm, EvaluationForm
from membership.models import UserMembership
from event.utils import make_ics,ics2response

from paypal.standard.ipn.models import *
import datetime, simplejson

filters = {
  "term": lambda: {
    "model": Term,
    "options": Term.objects.exclude(section__term__name__icontains='test'),
    "name": "Term",
    "slug": "term"
    },
  "subject": lambda: {
    "model": Subject,
    "options": Subject.objects.all(),
    "name": "Subject",
    "slug": "subject"
    }
  }

def index(request,term_id=None):
  term = Term.objects.all()[0]
  if term_id:
    term = Term.objects.get(pk=term_id)
    sessions = Session.objects.filter(section__term=term).select_related(depth=3)
  else:
    first_date = datetime.datetime.now()-datetime.timedelta(21)
    sessions = Session.objects.filter(first_date__gte=first_date).select_related(depth=3)
  user_sessions = []
  if request.user.is_authenticated():
    user_sessions = sessions.filter(enrollment__user=request.user.id)
    us_ids = [s.id for s in user_sessions]
    for session in sessions:
      if session.id in us_ids:
        try:
          session.user_enrollment = session.enrollment_set.filter(user=request.user)[0]
        except IndexError:
          pass
  sessions = sorted(list(sessions),key=lambda s: s.first_date)
  current_week = None
  weeks = {}
  all_sessions_closed = True
  for session in sessions:
    if current_week != session.get_week():
      current_week = session.get_week()
      weeks[current_week] = { 'open': 'closed', 0: current_week[0], 1: current_week[1], 'sessions': [] }
    weeks[current_week]['sessions'].append(session)
    if not session.closed:
      weeks[current_week]['open'] = 'open'
      all_sessions_closed = False

  values = {
    'weeks': sorted(weeks.values(),key=lambda i: i[0]),
    'sessions': sessions,
    'filters': [filters['subject']],
    'term': term,
    'all_sessions_closed': all_sessions_closed,
    'user_sessions': user_sessions,
    }
  return TemplateResponse(request,"course/classes.html",values)

def detail(request,slug):
  session = get_object_or_404(Session,slug=slug)
  enrollment = None
  if request.user.is_authenticated():
    enrollment = Enrollment.objects.filter(session=session,user=request.user)
  kwargs = dict(first_date__gte=datetime.datetime.now(),section__course=session.section.course)
  related_classes = Session.objects.filter(**kwargs).exclude(id=session.id)
  if request.POST:
    if not (request.user.is_superuser or request.user == session.user):
      messages.error(request,"Only an instructor can do that")
      return HttpResponseRedirect(request.path)
    ids = [int(i) for i in request.POST.getlist('completed')]
    for enrollment in session.enrollment_set.all():
      enrollment.completed = enrollment.id in ids
      enrollment.save()
    messages.success(request,"Course completion status saved for all students in this class.")
    return HttpResponseRedirect(request.path)
  values = {
    'session': session,
    'enrollment': enrollment,
    'related_classes': related_classes,
    }
  return TemplateResponse(request,"course/detail.html",values)

def ics_classes_all(request,fname):
  occurrences = ClassTime.objects.all()
  calendar_object = make_ics(occurrences,title="TX/RX Labs Classes")
  return ics2response(calendar_object,fname=fname)

@staff_member_required
def course_full(request):
  values = {
    'sessions': Session.objects.filter(first_date__gte=datetime.date.today()),
    }
  return TemplateResponse(request,"course/occupancy.html",values)

def course_totals(request):
  if not request.user.is_superuser:
    raise Http404
  term_list = []
  args = ('session','session__section','session__section__course','session__section__term')
  enrollments = Enrollment.objects.select_related(*args)
  for term in Term.objects.all():
    _dict = {
      'term': term,
      'sessions': {},
      'money': 0,
      'attendance': 0,
      }
    _enrollments = enrollments.filter(session__section__term=term)
    for e in _enrollments:
      session_dict = _dict['sessions'].get(e.session,{})
      session_dict['money'] = session_dict.get('money',0) + e.session.section.fee
      session_dict['attendance'] = session_dict.get('attendance',0) + e.quantity
      _dict['sessions'][e.session] = session_dict
      _dict['money'] += e.session.section.fee
      _dict['attendance'] += e.quantity
    term_list.append(_dict)
  values = { 'term_list': term_list }
  return TemplateResponse(request,'course/course_totals.html',values)

def rsvp(request,session_pk):
  session = get_object_or_404(Session,pk=session_pk)
  if session.section.fee > 0:
    raise ValueError("Some one tried to rsvp for a class that costs money!")
  enrollment,new = Enrollment.objects.get_or_create(user=request.user,session=session)
  if "drop" in request.GET:
    enrollment.delete()
    q = 0
    m = "You are no longer signed up for this."
  elif session.full:
    q = enrollment.quantity
    m = "Sorry, this event is full. Visit the class page to see when it will be offered again."    
  elif "plus_one" in request.GET:
    enrollment.quantity += 1
    enrollment.save()
    q = enrollment.quantity
    m = "You have RSVP'd for %s people. If you can't make it, please come back and unenroll."%q
    if session.full:
      m += "<br /> <b>This event is now full!</b>"
  else:
    q = 1
    m = "You have RSVP'd for this event. If you can't make it, please come back and unenroll."
  return HttpResponse(simplejson.dumps([q,m,session.full]))
