from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect

from course.models import Session
from membership.utils import limited_login_required
from .models import NotifyCourse

@login_required
def notify_course(request,session_id):
  session = Session.objects.get(pk=session_id)
  course = session.section.course
  defaults = {'session': session}
  _, new = NotifyCourse.objects.get_or_create(user=request.user,course=course,defaults=defaults)
  messages.success(request,"You will be emailed next time we teach {}".format(course))
  return HttpResponseRedirect(session.get_absolute_url())

@limited_login_required
def clear_notification(request,model_string,user_id,model_id):
  #! TODO: generalize
  model = NotifyCourse
  obj = model.objects.get(pk=model_id,user=request.limited_user)
  course = obj.course
  session = obj.session
  obj.delete()
  values = {
    'course': course,
    }
  messages.success(request,"You will not be emailed the next time we teach {}".format(course))
  return HttpResponseRedirect(session.get_absolute_url())
