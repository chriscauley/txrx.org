from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import QueryDict, Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from ..models import Course, Section, Term, Subject, Session, Enrollment, ClassTime
from ..forms import EmailInstructorForm, EvaluationForm
from membership.models import UserMembership
from notify.models import NotifyCourse
from db.utils import get_or_none
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
    "options": Subject.objects.filter(parent__isnull=True),
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
  subject_filters = filters['subject']()
  active_subjects = {}
  for session in sessions:
    session.set_user_fee(request.user)
    for subject in session.all_subjects:
      active_subjects[subject.pk] = active_subjects.get(subject.pk,0) + 1
  for subject in subject_filters['options']:
    subject.active_classes = active_subjects.get(subject.pk,0)
    subject.subfilters = []
    for child in subject.subject_set.all():
      child.active_classes = active_subjects.get(child.pk,0)
      if child.active_classes:
        subject.subfilters.append(child)
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
  user_sessions = sorted(list(user_sessions),key=lambda s: s.first_date)

  values = {
    'sessions': sessions,
    'filters': [subject_filters],
    'term': term,
    'user_sessions': user_sessions,
    'yesterday':datetime.datetime.now()-datetime.timedelta(0.5),
  }
  return TemplateResponse(request,"course/classes.html",values)

def detail(request,slug):
  session = get_object_or_404(Session,slug=slug)
  session.set_user_fee(request.user)
  enrollment = None
  notify_course = None
  if request.user.is_authenticated():
    enrollment = Enrollment.objects.filter(session=session,user=request.user)
    notify_course = get_or_none(NotifyCourse,user=request.user,course=session.section.course)
  kwargs = dict(first_date__gte=datetime.datetime.now(),section__course=session.section.course)
  alternate_sessions = Session.objects.filter(**kwargs).exclude(id=session.id)
  kwargs = dict(first_date__gte=datetime.datetime.now(),
                section__course__subjects__in=session.section.course.subjects.all())
  related_sessions = Session.objects.filter(**kwargs).exclude(id=session.id)
  related_sessions = [s for s in related_sessions if not (s.closed or s.full)]
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
    'alternate_sessions': alternate_sessions,
    'related_sessions': related_sessions,
    'notify_course': notify_course,
  }
  return TemplateResponse(request,"course/detail.html",values)

def ics_classes_all(request,fname):
  occurrences = ClassTime.objects.all()
  calendar_object = make_ics(occurrences,title="TX/RX Labs Classes")
  return ics2response(calendar_object,fname=fname)

def ics_classes_user(request,u_id,api_key,fname):
  user = get_object_or_404(get_user_model(),pk=u_id,usermembership__api_key=api_key)
  enrollments = user.enrollment_set.all()
  sessions = [e.session for e in enrollments]
  sessions += user.session_set.all()
  occurrences = []
  for session in sessions:
    occurrences += session.classtime_set.all()
  calendar_object = make_ics(occurrences,title="[TX/RX] My Classes")
  return ics2response(calendar_object,fname=fname)

@staff_member_required
def course_full(request):
  dt = datetime.date.today()-datetime.timedelta(14)
  values = {
    'sessions': Session.objects.filter(first_date__gte=dt).order_by('first_date'),
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
  if not request.user.is_authenticated():
    m = "You must be logged in to rsvp. Click the icon at the top right of the page to login or register"
    return HttpResponse(simplejson.dumps([0,m,session.full]))
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

def start_checkout(request):
  cart_items = simplejson.loads(request.GET['cart'])
  out = []
  for cart_item in cart_items:
    session = Session.objects.get(pk=cart_item['pk'])
    new_total = session.total_students + cart_item['quantity']
    if new_total > session.section.max_students:
      out.append({'pk': session.pk,'remaining': session.section.max_students-session.total_students})
  return HttpResponse(simplejson.dumps(out))
