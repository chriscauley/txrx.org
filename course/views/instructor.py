from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from ..models import Session
from ..forms import EmailInstructorForm
from lablackey.utils import FORBIDDEN

import datetime

@login_required
def email(request,session_pk):
  session = get_object_or_404(Session,pk=session_pk)
  form = EmailInstructorForm(session,request)
  if request.POST and form.is_valid():
    form.send()
  values = {'form': form}
  return TemplateResponse(request,"course/email_instructor.html",values)

@login_required
def session(request,session_pk):
  allowed = request.user.groups.filter(name="Class Coordinator")
  allowed = allowed or request.user.is_superuser
  session = get_object_or_404(Session,pk=session_pk)
  allowed = allowed or request.user == session.user
  if not allowed:
    return FORBIDDEN
  values = {'session': session}
  if request.POST:
    if not (request.user.is_superuser or request.user == session.user):
      messages.error(request,"Only an instructor can do that")
      return HttpResponseRedirect(request.path)
    ids = [int(i) for i in request.POST.getlist('completed')]
    for enrollment in session.enrollment_set.all():
      if enrollment.id in ids:
        enrollment.completed = datetime.datetime.now()
      elif enrollment.completed:
        enrollment.completed = None
      enrollment.save()
    messages.success(request,"Course completion status saved for all students in this class.")
    return HttpResponseRedirect(request.path)
  return TemplateResponse(request,"course/instructor_session.html",values)
