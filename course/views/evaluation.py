from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import QueryDict, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from ..models import Course, Term, Subject, Session, Enrollment, ClassTime, Evaluation
from ..forms import EmailInstructorForm, EvaluationForm
from membership.models import UserMembership
from event.utils import make_ics,ics2response

from paypal.standard.ipn.models import *

@login_required
def index(request):
  pending_evaluations = Enrollment.objects.pending_evaluation(user=request.user)
  values = {
    'pending_evaluations': pending_evaluations
  }
  return TemplateResponse(request,"course/evaluations.html",values)

@login_required
def detail(request,enrollment_id):
  enrollment = get_object_or_404(Enrollment,pk=enrollment_id,user=request.user)
  form = EvaluationForm(request.POST or None,enrollment=enrollment)
  if request.POST and form.is_valid():
    evaluation = form.save(commit=False)
    evaluation.user = request.user
    evaluation.enrollment = enrollment
    evaluation.save()
    messages.success(request,"Your evaluation has been submitted. Thank you for your feedback!")
    return HttpResponseRedirect(reverse("course:evaluation_index"))
  values = { 'enrollment': enrollment, 'form': form }
  return TemplateResponse(request,"course/evaluation_form.html",values)

@login_required
def refuse(request,enrollment_id):
  enrollment = get_object_or_404(Enrollment,pk=enrollment_id,user=request.user)
  enrollment.evaluated = True
  enrollment.save()
  messages.success(request,"You have opted not to evaluate a class.")
  return HttpResponseRedirect(reverse("course:evaluation_index"))

@login_required
def instructor_detail(request,instructor_id=None):
  if not request.user.is_staff or (not instructor_id and not request.user.is_superuser):
    return HttpResponseNotAllowed()
  if not instructor_id:
    instructor_id = request.user.id
  sessions = Session.objects.filter(user_id=instructor_id).order_by("-first_date")
  session_evaluations = []
  for session in sessions:
    evaluations = Evaluation.objects.filter(enrollment__session=session)
    if not evaluations:
      continue
    session_evaluations.append((session,evaluations))
  values = {'session_evaluations': session_evaluations}
  return TemplateResponse(request,"course/instructor_evaluations.html",values)
