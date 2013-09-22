from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import QueryDict, Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from .models import Course, Section, Term, Subject, Session, Enrollment, ClassTime
from .forms import EmailInstructorForm, EvaluationForm
from membership.models import UserMembership
from event.utils import make_ics,ics2response

from djpjax import pjaxtend
from paypal.standard.ipn.models import *

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
  sessions = Session.objects.filter(section__term=term).select_related(depth=2)
  sessions = sorted(list(sessions),key=lambda s: s.first_date)
  test_session = Session.objects.get(section__term__name__iexact="test term") #the test term
  user_sessions = []
  current_week = None
  weeks = {}
  all_sessions_closed = True
  for session in sessions:
    if current_week != session.week:
      current_week = session.week
      weeks[current_week] = { 'open': 'closed', 0: current_week[0], 1: current_week[1], 'sessions': [] }
    weeks[current_week]['sessions'].append(session)
    if not session.closed:
      weeks[current_week]['open'] = 'open'
      all_sessions_closed = False
  if request.user.is_authenticated():
    user_sessions = Session.objects.filter(enrollment__user=request.user.id)
  values = {
    'weeks': sorted(weeks.values(),key=lambda i: i[0]),
    'sessions': sessions,
    'filters': [filters['subject']],
    'term': term,
    'user_sessions': user_sessions,
    'all_sessions_closed': all_sessions_closed,
    'test_session': test_session,
    'parent': 'base.html',
    }
  return TemplateResponse(request,"course/classes.html",values)

@pjaxtend()
def detail(request,slug):
  session = get_object_or_404(Session,slug=slug)
  enrollment = None
  if request.user.is_authenticated():
    enrollment = Enrollment.objects.filter(session=session,user=request.user)
  values = {
    'session': session,
    'enrollment': enrollment,
    }
  return TemplateResponse(request,"course/detail.html",values)

@pjaxtend()
def instructors(request,username=None):
  instructors = UserMembership.objects.list_instructors()
  values = {'instructors':instructors}
  return TemplateResponse(request,"course/instructors.html",values)

@pjaxtend()
def instructor_detail(request,username=None):
  profile = UserMembership.objects.get(user__username=username)
  values = {
    'profile': profile
    }
  return TemplateResponse(request,"course/instructor_detail.html",values)

@login_required
@pjaxtend()
def my_sessions(request):
  instructor = request.user
  current_term = Term.objects.all()[0]
  terms = Term.objects.all()
  enrollment_tuples = []
  teaching_tuples = []
  for term in terms:
    enrollments = Enrollment.objects.filter(user=request.user,session__section__term=term)
    sessions = Session.objects.filter(user=instructor,section__term=term)
    if enrollments:
      enrollment_tuples.append((enrollments,term))
    if sessions:
      teaching_tuples.append((sessions,term))
  values = {
    'instructor': instructor,
    'teaching_tuples': teaching_tuples,
    'enrollment_tuples': enrollment_tuples,
    'current_term': current_term,
    }
  return TemplateResponse(request,"course/my_sessions.html",values)
  
@staff_member_required
def all_sessions(request):
  current_term = Term.objects.all()[0]
  sessions = Session.objects.filter(section__term=current_term)
  
  total_fees = 0
  total_enrollments = 0
  for session in sessions:
      enrollments = session.enrollment_set.count()
      class_price = session.section.fee
      total_enrollments += enrollments
      total_fees += enrollments * class_price
  
  values = {
    'sessions': sessions,
    'current_term': current_term,
    'total_enrollments': total_enrollments,
    'total_fees': total_fees,
    }
  return TemplateResponse(request,"course/all_sessions.html",values)

@login_required
def evaluation_index(request):
  enrollments = Enrollment.objects.filter(evaluated=False,user=request.user)
  return TemplateResponse(request,"course/evaluations.html",{'enrollments': enrollments})

@login_required
def evaluation_detail(request,enrollment_id):
  enrollment = get_object_or_404(Enrollment,pk=enrollment_id,user=request.user)
  form = EvaluationForm(request.POST or None)
  if request.POST and form.is_valid():
    evaluation = form.save()
    messages.success(request,"Your evaluation has been submitted. Thank you for your feedback!")
    return HttpResponseRedirect(reverse("evaluation_index"))
  values = { 'enrollment': enrollment, 'form': form }
  return TemplateResponse(request,"course/evaluation_form.html",values)

def debug_parsing(request, id):
  ipn = PayPalIPN.objects.get(id=id)

  query = ipn.query
  #add them to the classes they're enrolled in
  params = QueryDict(ipn.query)
  class_count = int(params['num_cart_items'])
  course_info = []

  for i in range(1, class_count+1):
    session_id = int(params['item_number%d' % (i, )])
    section_cost = int(float(params['mc_gross_%d' % (i, )]))
    session = Session.objects.get(id=session_id)
    course_info.append((session_id, section_cost))

    return TemplateResponse(request,"course/debug.html",locals())

def email_instructor(request,session_pk):
  session = get_object_or_404(Session,pk=session_pk)
  form = EmailInstructorForm(session,request)
  if request.POST and form.is_valid():
    form.send()
  values = {'form': form}
  return TemplateResponse(request,"course/email_instructor.html",values)

def ics_classes_all(request,fname):
  occurrences = ClassTime.objects.all()
  calendar_object = make_ics(occurrences,title="TX/RX Labs Classes")
  return ics2response(calendar_object,fname=fname)

def course_totals(request):
  if not request.user.is_superuser:
    raise Http404
  dicts = {}
  args = ('session','session__section','session__section__course','session__section__course__term')
  enrollments = Enrollment.objects.select_related(*args)
  for e in enrollments:
    session_dict = dicts.get(e.session,{})
    session_dict['money'] = session_dict.get('money',0) + e.session.section.fee
    session_dict['attendance'] = session_dict.get('attendance',0) + e.quantity
    dicts[e.session] = session_dict
  values = {'course_tuples':[(k,v['money'],v['attendance']) for k,v in dicts.items()]}
  return TemplateResponse(request,'course/course_totals.html',values)
