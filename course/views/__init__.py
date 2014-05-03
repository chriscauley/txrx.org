from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import QueryDict, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from ..models import Course, Section, Term, Subject, Session, Enrollment, ClassTime
from ..forms import EmailInstructorForm, EvaluationForm
from db.utils import get_or_none
from event.utils import make_ics,ics2response
from membership.models import UserMembership

from paypal.standard.ipn.models import *

@login_required
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

def paypal_return(request):
  session_ids = [v for k,v in request.REQUEST.items() if k.startswith('item_number')]
  if not ('payer_email' in request.REQUEST) or not session_ids:
    raise Http404
  email = request.REQUEST['payer_email']
  sessions = Session.objects.filter(pk__in=session_ids)
  matched_user = None
  if not request.user.is_authenticated():
    matched_user = get_or_none(User,email=email)
    matched_user = matched_user or get_or_none(User,usermembership__paypal_email=email)
  values = {
    'email': email,
    'sessions': sessions,
    'matched_user': matched_user,
  }
  return TemplateResponse(request,"course/paypal_return.html",values)
