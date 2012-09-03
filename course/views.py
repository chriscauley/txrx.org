from django.template.response import TemplateResponse
from course.models import Course, Section, Term, Subject, Session
from membership.models import Profile
from django.http import QueryDict

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
  sessions = sorted(list(Session.objects.filter(section__term=term)),key=lambda s: s.first_date())
  values = {
    'sessions': sessions,
    'filters': [filters['term'],filters['subject']],
    'term': term,
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


def debug_parsing(request, id):
    ipn = PayPalIPN.objects.get(id=id)

    query = ipn.query
    #add them to the classes they're enrolled in
    params = QueryDict(ipn.query)

    class_count = int(params['num_cart_items'])

    course_info = []

    for i in range(1, class_count+1):
        session_id = int(params['item_number%d' % (i, )])
        #section_cost = int(float(params['mc_gross_%d' % (i, )]))

        session = Session.objects.get(id=session_id)

        course_info.append(session_id)
    

    return TemplateResponse(request,"course/debug.html",locals())
