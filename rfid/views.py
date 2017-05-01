from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from .models import RFIDLog
from membership.models import Level, Subscription, SubscriptionBuddy
from tool.models import Permission, Tool, APIKey, DoorGroup, Schedule, Holiday

import datetime, json

FAIL = HttpResponse('{"status": 403, "message": "I am Vinz Clortho keymaster of Gozer... Gozer the Traveller, he will come in one of the pre-chosen forms. During the rectification of the Vuldronaii, the Traveller came as a large and moving Torb! Then, during the third reconciliation of the last of the Meketrex Supplicants they chose a new form for him... that of a Giant Sloar! many Shubs and Zulls knew what it was to be roasted in the depths of the Sloar that day I can tell you."}',status=403)

def valid_ip_or_api_key(request):
  key = getattr(request,request.method.upper()).get('api_key')
  valid = request.META['REMOTE_ADDR'] in getattr(settings,'DOOR_IPS',[])
  valid = valid or APIKey.objects.filter(key=key)
  return valid or APIKey.objects.filter(key=key)

def rfid_log(request):
  if not valid_ip_or_api_key(request):
    return FAIL
  DATA = getattr(request,request.method.upper())
  if not ('logs' in DATA):
    return HttpResponse('{"message": "Need logs parameter.","status": 400}',status=400)
  out = []
  for d in json.loads(DATA['logs']):
    log = RFIDLog.objects.create(
      data=d,
      rfid_number=d['rfid'],
    )
    out.append({
      "rfid": log.rfid_number,
      "data": log.data,
      "status": 200
    })
  return JsonResponse({'logs_created': out})

def door_access(request):
  valid = valid_ip_or_api_key(request)
  if not valid and not request.user.is_authenticated():
    return FAIL
  valid = valid or request.user.is_superuser

  _Q = Q(canceled__isnull=True) | Q(paid_until__gte=datetime.datetime.now())
  base_subs = Subscription.objects.filter(_Q,owed__lte=0)
  base_subs = base_subs.exclude(user__rfid__isnull=True)
  base_sub_buddies = SubscriptionBuddy.objects.filter(paid_until__gte=datetime.datetime.now())

  obj = None
  out = {
    'schedule': {},
    'rfids': {},
    'holidays': {}
  }

  #fieldname is intended to be used only for testing
  fieldname = request.GET.get('fieldname','rfid__number')
  if fieldname in ['email','paypal_email','password']:
    return FAIL

  if 'permission_id' in request.GET:
    obj = get_object_or_404(Permission,id=request.GET['permission_id'])
    valid = valid or request.user.is_toolmaster
    superQ = Q(is_superuser=True)|Q(is_toolmaster=True)

    # only return subscriptions where the user has this permission
    base_subs = base_subs.filter(user_id__in=obj.get_all_user_ids())

  if 'door_id' in request.GET:
    obj = get_object_or_404(DoorGroup,id=request.GET['door_id'])
    valid = valid or request.user.is_gatekeeper
    superQ = Q(is_superuser=True)|Q(is_gatekeeper=True)
    _hids = [99999]+list(Level.objects.filter(holiday_access=True).values_list("id",flat=True))
    _hids = [str(h) for h in _hids]
    out['holidays'] = { h.date.strftime("%Y-%m-%d"):_hids for h in Holiday.objects.all()}

  if not (valid and obj):
    return FAIL

  schedule_jsons = { s.id: s.as_json for s in Schedule.objects.all() }
  for level in Level.objects.all():
    subscriptions = base_subs.filter(level=level).distinct()
    out['rfids'][level.order] = list(subscriptions.values_list('user__'+fieldname,flat=True))
    _Q = Q(level_override__isnull=True,subscription__level=level) | Q(level_override=level)
    sub_buddies = base_sub_buddies.filter(_Q)
    out['rfids'][level.order] += list(sub_buddies.values_list('user__'+fieldname,flat=True))
    out['schedule'][level.order] = schedule_jsons.get(level.get_schedule_id(obj),{})

  staff = get_user_model().objects.filter(superQ).exclude(rfid__isnull=True)
  out['rfids'][99999] = list(staff.values_list(fieldname,flat=True))
  out['schedule'][99999] = schedule_jsons[settings.ALL_HOURS_ID]
  if 'door_id' in request.GET:
    volunteers = get_user_model().objects.filter(is_active=True,is_volunteer=True)
    out['rfids'][99998] = list(volunteers.values_list(fieldname,flat=True))
    out['schedule'][99998] = schedule_jsons[1]
  if 'api_key' in request.GET:
    return HttpResponse(json.dumps(out))
  return HttpResponse("<pre>%s</pre>"%json.dumps(out,indent=4))

@staff_member_required
def permission_table(request):
  permissions = Permission.objects.all().order_by("name")
  permissions_tools = [(p,p.tool_set.all().order_by('name')) for p in permissions]
  permissions_tools.append((None,Tool.objects.filter(permission=None).order_by('name')))
  values = {
    'permission_tools': permissions_tools,
    'levels': Level.objects.all(),
    'doorgroups': DoorGroup.objects.all()
  }
  return TemplateResponse(request,'membership/rfid_permission_table.html',values)
