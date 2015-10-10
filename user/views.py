from django.http import HttpResponse
from django.template.response import TemplateResponse
from .models import User, UserCheckin
from geo.models import Room

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
