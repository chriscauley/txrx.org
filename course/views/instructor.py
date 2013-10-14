from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import QueryDict, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from ..models import Course, Section, Term, Subject, Session, Enrollment, ClassTime
from ..forms import EmailInstructorForm, EvaluationForm
from membership.models import UserMembership
from event.utils import make_ics,ics2response

from djpjax import pjaxtend
from paypal.standard.ipn.models import *

@pjaxtend()
def index(request,username=None):
  instructors = UserMembership.objects.list_instructors()
  values = {'instructors':instructors}
  return TemplateResponse(request,"course/instructors.html",values)

@pjaxtend()
def detail(request,username=None):
  profile = UserMembership.objects.get(user__username=username)
  values = {
    'profile': profile
    }
  return TemplateResponse(request,"course/instructor_detail.html",values)

def email(request,session_pk):
  session = get_object_or_404(Session,pk=session_pk)
  form = EmailInstructorForm(session,request)
  if request.POST and form.is_valid():
    form.send()
  values = {'form': form}
  return TemplateResponse(request,"course/email_instructor.html",values)
