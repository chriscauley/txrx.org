from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import QueryDict
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from course.models import Course, Section, Term, Subject, Session, Enrollment
from membership.models import UserMembership

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

def index(request,term_id):
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
  values = {
    'session': session
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
  sessions = Session.objects.filter(user=instructor,section__term=current_term)
  enrollments = Enrollment.objects.filter(user=request.user,session__section__term=current_term)
  values = {
    'instructor': instructor,
    'sessions': sessions,
    'enrollments': enrollments,
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
