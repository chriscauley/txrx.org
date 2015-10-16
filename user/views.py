from django.http import HttpResponse
from django.template.response import TemplateResponse

from .models import User, UserCheckin
from course.models import Enrollment
from geo.models import Room
from tool.models import UserCriterion, Permission

import json, datetime

def checkin(request):
  if not request.is_ajax():
    return TemplateResponse(request,"checkin.html",{})
  try:
    user = User.objects.get(rfid=request.GET.get('rfid','no one has this as an rfid'))
  except User.DoesNotExist:
    return HttpResponse(json.dumps({'status': 404}))
  defaults = {'content_object': Room.objects.get(name='')}
  checkin, new = UserCheckin.objects.get_or_create(user=user,time_out__isnull=True,defaults=defaults)
  if not new:
    checkin.time_out = datetime.datetime.now()
    checkin.save()

  out = {
    'user': user.username,
    'time_in': str(checkin.time_in),
    'time_out': str(checkin.time_out) if checkin.time_out else None,
  }
  return HttpResponse(json.dumps(out))

def user_json(request):
  if not request.user:
    return TemplateResponse(request,"user.json",{'user_json':'{}'});
  enrollments = Enrollment.objects.filter(user=request.user,completed=True)
  usercriteria = UserCriterion.objects.filter(user=request.user)
  values = {
    'user_json': {
      'pk': request.user.pk,
      'permission_ids': [p.pk for p in Permission.objects.all() if p.check_for_user(request.user)],
      'criterion_ids': list(usercriteria.values_list('criterion_id',flat=True)),
      'completed_course_ids': [e.session.course_id for e in enrollments],
    }
  }
  return TemplateResponse(request,"user.json",values)
