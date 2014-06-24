from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from ..models import Session
from ..forms import EmailInstructorForm

def email(request,session_pk):
  session = get_object_or_404(Session,pk=session_pk)
  form = EmailInstructorForm(session,request)
  if request.POST and form.is_valid():
    form.send()
  values = {'form': form}
  return TemplateResponse(request,"course/email_instructor.html",values)
