from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from .models import User, UserCheckin
from course.models import Enrollment
from geo.models import Room
from tool.models import Criterion, UserCriterion, Permission

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
    return TemplateResponse(request,"user.json",{'user_json':'null'});
  enrollments = Enrollment.objects.filter(user=request.user,completed=True)
  usercriteria = UserCriterion.objects.filter(user=request.user)
  _c = Criterion.objects.filter(courses__session__user=request.user).distinct()
  master_criterion_ids = list(_c.values_list('id',flat=True))
  values = {
    'user_json': json.dumps({
      'pk': request.user.pk,
      'permission_ids': [p.pk for p in Permission.objects.all() if p.check_for_user(request.user)],
      'criterion_ids': list(usercriteria.values_list('criterion_id',flat=True)),
      'master_criterion_ids': master_criterion_ids,
      'session_ids': list(request.user.session_set.all().values_list('id',flat=True)),
      'completed_course_ids': [e.session.course_id for e in enrollments],
      'is_toolmaster': request.user.is_toolmaster
    })
  }
  return TemplateResponse(request,"user.json",values)

@staff_member_required
def set_rfid(request):
  user = get_object_or_404(get_user_model(),pk=request.GET['user_id'])
  old_rfid = user.rfid
  user.rfid = request.GET['rfid']
  user.save()
  return HttpResponse(json.dumps(old_rfid))
