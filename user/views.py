from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.static import serve

from .models import User, UserCheckin
from rfid.models import RFID
from event.models import RSVP
from course.models import Enrollment, ClassTime
from course.utils import get_or_create_student
from geo.models import Room
from membership.utils import temp_user_required
from redtape.models import Document
from tool.models import Criterion, UserCriterion, Permission

from lablackey.utils import get_or_none
from sorl.thumbnail import get_thumbnail
import json, datetime, os, binascii

def checkin_json(user):
  today = datetime.date.today()
  tomorrow = today + datetime.timedelta(1)
  if settings.DEBUG:
    tomorrow = tomorrow+datetime.timedelta(10)
  _q = Q(session__enrollment__user=user) | Q(session__user=user)
  _ct = ClassTime.objects.filter(_q,start__gte=today,start__lte=tomorrow).distinct()
  _sq = Q(canceled__gte=datetime.datetime.now()-datetime.timedelta(90)) | Q(canceled__isnull=True)
  _s = user.subscription_set.filter(_sq).order_by("-canceled")
  if True: #user.level and user.level.order >= 10:
    required_document_ids = getattr(settings,"REQUIRED_DOCUMENT_IDS",[])
  else:
    required_document_ids = getattr(settings,"NONMEMBER_DOCUMENT_IDS",[])
  documents = [d.get_json_for_user(user) for d in Document.objects.filter(id__in=required_document_ids)]
  return {
    'classtimes': [c.as_json for c in _ct],
    'sessions': {c.session_id: c.session.as_json for c in _ct},
    'permission_ids': [p.pk for p in Permission.objects.all() if p.check_for_user(user)],
    'user_id': user.id,
    'user_display_name': user.get_full_name(),
    'subscriptions': [s.as_json for s in _s],
    'documents': documents,
    'thumbnail': get_thumbnail(user.headshot,"200x300",crop="center").url if user.headshot else None
  }

@staff_member_required
def todays_checkins_json(request):
  checkins = UserCheckin.objects.filter(time_in__gte=datetime.datetime.now().replace(hour=0,minute=0))
  return JsonResponse({'todays_ids': list(checkins.values_list("ids",flat=True))})

@staff_member_required
def user_checkin(request):
  user = User.objects.get(id=request.GET['user_id'])
  return JsonResponse(checkin_json(user))

@temp_user_required
def checkin_ajax(request):
  messages = []
  user = request.temp_user
  defaults = {'content_object': Room.objects.get(name='')}
  if not request.POST.get('no_checkin',None):
    checkin, new = UserCheckin.objects.checkin_today(user=user,defaults=defaults)
    t = "%s checked in on %s. Please take a moment to review your permissions, membership level, and upcoming classes below. If anything appears wrong please contact the staff. Click 'Done' when you are finished so that the next person can check in."
    messages.append({'level': 'success', 'body': t%(user,checkin.time_in.date())})
  out = {
    'messages': messages,
    'checkin': checkin_json(user),
    'rfid': request.POST.get('rfid',None),
  }
  return JsonResponse(out)

def checkin_email(request):
  user = User.objects.get_from_anything(request.POST["email"])
  if not user:
    return JsonResponse({"next": "checkin-new-user","email": request.POST["email"]})
  defaults = { 'content_object': Room.objects.get(name='') }
  checkin, new = UserCheckin.objects.checkin_today(user=user,defaults=defaults)
  return JsonResponse({ "checkin": checkin_json(user), "badge": True })

def add_rfid(request):
  rfid = request.POST['new_rfid']
  user = get_user_model().objects.get_from_anything(request.POST.get("username",None))
  user and user.check_password(request.POST.get('password',''))
  if not user:
    return JsonResponse({'error': "Username and password do not match"},status=401)
  if user.rfid_set.count():
    m = 'You already have an RFID card registered. Please see staff if you need to change cards.'
    return JsonResponse({'error': m})
  RFID.objects.get_or_create(user=user,number=rfid)
  messages = [{'level': 'success', 'body': 'RFID set. Please swipe now to checkin.'}]
  return JsonResponse({'messages': messages})

def checkin_register(request):
  keys = ['email','first_name','last_name',"password"]
  user,new = get_or_create_student({k: request.POST[k] for key in keys})

def user_json(request):
  if not request.user.is_authenticated():
    return JsonResponse({})
  enrollments = Enrollment.objects.filter(user=request.user,completed__isnull=False)
  usercriteria = UserCriterion.active_objects.filter(user=request.user)
  _c = Criterion.objects.filter(courses__session__user=request.user).distinct()
  master_criterion_ids = list(_c.values_list('id',flat=True))
  keys = [
    'id','email','username','first_name','last_name','is_toolmaster','is_shopkeeper','is_staff','is_superuser'
  ]
  out = { k: getattr(request.user,k) for k in keys }
  out.update({
    'permission_ids': [p.pk for p in Permission.objects.all() if p.check_for_user(request.user)],
    'criterion_ids': list(usercriteria.values_list('criterion_id',flat=True)),
    'master_criterion_ids': master_criterion_ids,
    'session_ids': list(request.user.session_set.all().values_list('id',flat=True)),
    'completed_course_ids': [e.session.course_id for e in enrollments],
    'enrollments': {e.session_id:e.quantity for e in request.user.enrollment_set.all()},
    'enrolled_course_ids': list(request.user.enrollment_set.all().values_list("session__course_id",flat=True)),
    'member_discount_percent': request.user.level.discount_percentage,
  })
  return JsonResponse({'user': out});

@staff_member_required
def set_rfid(request):
  user = get_object_or_404(get_user_model(),pk=request.GET['user_id'])
  error = None
  number = request.GET['rfid']
  try:
    RFID.objects.get_or_create(user=user,number=number)
  except IntegrityError:
    error = "%s is already in use by %s"%(number,RFID.objects.get(number=number).user)
  response = {
    'rfids': list(RFID.objects.filter(user=user).values_list("number",flat=True)),
    'error': error,
  }
  return JsonResponse(response)

@staff_member_required
def remove_rfid(request):
  user = get_object_or_404(get_user_model(),pk=request.GET['user_id'])
  RFID.objects.get(user=user,number=request.GET['rfid']).delete()
  response = {
    'rfids': list(RFID.objects.filter(user=user).values_list("number",flat=True)),
  }
  return JsonResponse(response)

@staff_member_required
def hidden_image(request):
  path = request.path.split(settings.STAFF_URL)[-1]
  if request.path.startswith("/superuser_images/") and not request.user.is_superuser():
    return HttpResponse("Not Allowed",status=403)
  return serve(request, path, settings.STAFF_ROOT)

@staff_member_required
def change_headshot(request,attr):
  user = get_object_or_404(get_user_model(),pk=request.POST['user_id'])
  f = request.FILES.get(attr,None) # if somehow they upload the uncompressed image
  fname = "%s-%s.jpg"%(attr,user.id)
  if request.POST.get('blob',None):
    f = ContentFile(request.POST['blob'].split(",")[1].decode('base64'))
  if attr == 'headshot':
    user.headshot.save(fname,f)
    user.save()
  elif attr == 'id_photo':
    admin_url = "https://txrxlabs.org/admin/user/user/%s"%user.id
    msg = EmailMessage(
      user.username,
      "\n".join([str(s) for s in [user.get_full_name(),user.email,user.paypal_email,admin_url]]),
      settings.DEFAULT_FROM_EMAIL,
      [settings.ID_PHOTO_EMAIL]
    )
    msg.attach(fname,f.read(),'image/jpg')
    msg.send()
    user.id_photo_date = datetime.date.today()
    user.save()
    attr = 'id_photo_date'
  return JsonResponse({'done': str(getattr(user,attr))})
