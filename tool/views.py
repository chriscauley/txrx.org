from django.apps import apps
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from course.models import Enrollment, CourseEnrollment
from geo.models import Room
from redtape.models import Signature
from tool.models import Tool, Lab, Group, Permission, Criterion, UserCriterion

from user.models import is_toolmaster

import json, datetime

def lab_index(request):
  values = {'labs': Lab.objects.all()}
  return TemplateResponse(request,'tool/lab_index.html',values)

def lab_detail(request,lab_slug,pk):
  values = {'lab': get_object_or_404(Lab,pk=pk) }
  return TemplateResponse(request,'tool/lab_detail.html',values)

def tool_detail(request,tool_slug,pk):
  tool = get_object_or_404(Tool,pk=pk)
  values = {
    'tool': tool,
    'lab': tool.lab,
  }
  return TemplateResponse(request,'tool/tool_detail.html',values)

@staff_member_required
def toggle_criterion(request):
  User = get_user_model()
  user = get_object_or_404(User,pk=request.GET['user_id'])
  if request.GET.get('criterion_id'):
    criterion = get_object_or_404(Criterion,pk=request.GET['criterion_id'])
    if not criterion.user_can_grant(request.user):
      return HttpResponseForbidden("You do not have permission to assign this criterion.")
    ucs = UserCriterion.active_objects.filter(criterion=criterion,user=user)

    if ucs:
      ucs.delete()
    else:
      defaults = {'content_object': request.user}
      UserCriterion.active_objects.get_or_create(criterion=criterion,user=user,defaults=defaults)
  obj = None
  if request.GET.get('enrollment_id'):
    obj = get_object_or_404(Enrollment,pk=request.GET["enrollment_id"])
  if request.GET.get('signature_id'):
    obj = get_object_or_404(Signature,pk=request.GET["signature_id"])
  if request.GET.get('courseenrollment_id'):
    obj = get_object_or_404(CourseEnrollment,pk=request.GET["courseenrollment_id"])

  if obj:
    if not obj.has_completed_permission(request.user):
      return HttpResponseForbidden("You do not have permission to modify this object")
    obj.completed = None if obj.completed else datetime.datetime.now()
    obj.save()
  # send back the new user criterion ids to replace old data
  user = User.objects.get(pk=user.pk)
  attrs = ['signature_jsons','enrollment_jsons','locked_criterion_ids','usercriterion_jsons','courseenrollment_jsons']
  return JsonResponse({attr: getattr(user,attr) for attr in attrs})

def checkout_items(request):
  room_items = [(r,r.checkoutitem_set.all()) for r in Room.objects.all()]
  values = {'room_items': filter(lambda i:i[1],room_items)}
  return TemplateResponse(request,"tool/checkout_items.html",values)

@user_passes_test(is_toolmaster)
def master(request,app_name,model_name):
  model = apps.get_app_config(app_name).get_model(model_name)
  objs = model.objects.user_controls(request.user)

  if request.GET.get('user_search',''):
    user_ids = get_user_model().objects.keyword_search(request.GET['user_search'])
    objs = objs.filter(user_id__in=user_ids)
  elif "object_id" in request.GET:
    objs = objs.filter(object_id=request.GET['object_id'])
  objs = objs.distinct()

  if request.POST:
    try:
      obj = objs.get(pk=request.POST['object_id'])
    except model.DoesNotExist:
      raise NotImplementedError("%s cannot edit %s with id #%s"%(request.user,model,request.POST['pk']))
    obj.completed = obj.failed = None
    action = request.POST.get('action',None).lower() or "incomplete"
    if action == "pass":
      obj.completed = datetime.datetime.now()
    elif action == "fail":
      obj.failed = datetime.datetime.now()
    obj.save()
    out = obj.as_json
    out['message'] = '%s marked as "%s".'%(obj,action)
    return JsonResponse(out)
  cutoff = datetime.datetime.now()-datetime.timedelta(60)
  objs = objs.filter(datetime__gte=cutoff)
  events = {}
  for obj in objs:
    if not obj.content_object in events:
      events[obj.content_object] = []
    events[obj.content_object].append(obj.as_json)
  events = [{
    'name': unicode(event),
    'objects': objects,
  } for event,objects in events.items()]
  values = {
    'events': json.dumps(events,cls=DjangoJSONEncoder),
    'model_slug': "%s.%s"%(app_name,model_name),
  }
  return TemplateResponse(request,'tool/master.html',values)
