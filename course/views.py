from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import QueryDict
from course.models import Course, Section, Term, Subject, Session
from membership.models import Profile

from paypal.standard.ipn.models import *

filters = {
  "term": lambda: {
    "model": Term,
    "options": Term.objects.all(),
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

def index(request):
  term = Term.objects.all()[0]
  sessions = Session.objects.filter(section__term=term).select_related(depth=2)
  sessions = sorted(list(sessions),key=lambda s: s.first_date)
  user_sessions = []
  if request.user.is_authenticated():
    user_sessions = Session.objects.filter(enrollment__user=request.user.id)
  values = {
    'sessions': sessions,
    'filters': [filters['term'],filters['subject']],
    'term': term,
    'user_sessions': user_sessions
    }
  return TemplateResponse(request,"course/classes.html",values)

def instructors(request,username=None):
  instructors = Profile.objects.list_instructors()
  values = {'instructors':instructors}
  return TemplateResponse(request,"course/instructors.html",values)

def instructor_detail(request,username=None):
  profile = Profile.objects.get(user__username=username)
  values = {
    'profile': profile
    }
  return TemplateResponse(request,"course/instructor_detail.html",values)

@login_required
def my_sessions(request):
  instructor = request.user
  #need to filter this to show only future classes (not done yet) and show it soonest class first
  sessions = Session.objects.filter(user=instructor)
  current_term = Term.objects.all()[0]
  values = {
    'instructor': instructor,
    'sessions': sessions,
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
      enrollments = session.enrollments_set.count()
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
