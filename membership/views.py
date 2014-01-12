from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from .models import Membership, MeetingMinutes, Officer
from .forms import UserForm, UserMembershipForm, RegistrationForm
from .utils import limited_login_required

from course.models import Course,CourseCompletion
from txrx.utils import FORBIDDEN

from registration.views import register as _register
import datetime

def join_us(request):
  values = {
    'memberships': Membership.objects.active(),
    'flatpage':lambda:FlatPage.objects.get(url='/join-us/'),
    }
  return TemplateResponse(request,"membership/join-us.html",values)

@login_required
def user_settings(request):
  user = request.user
  user_form = UserForm(request.POST or None, instance=user)
  user_membership = user.usermembership
  usermembership_form = UserMembershipForm(request.POST or None, request.FILES or None, instance=user_membership)
  if request.POST and all([user_form.is_valid(),usermembership_form.is_valid()]):
    user_form.save()
    usermembership_form.save()
    messages.success(request,'Your settings have been saved.')
    return HttpResponseRedirect(request.path)
  values = {
    'forms': [user_form, usermembership_form],
    }
  return TemplateResponse(request,'membership/settings.html',values)

@login_required
def minutes(request,datestring):
  date = datetime.datetime.strptime(datestring,"%Y-%m-%d")
  minutes = get_object_or_404(MeetingMinutes,date=date)
  values = {
    'minutes': minutes,
    }
  return TemplateResponse(request,'membership/minutes.html',values)

@login_required
def minutes_index(request):
  values = {
    'minutes_set': MeetingMinutes.objects.all(),
    }
  return TemplateResponse(request,'membership/minutes_index.html',values)

def register(request,*args,**kwargs):
  kwargs['form_class'] = RegistrationForm
  if request.POST and request.POST.get('email',None):
    email = request.POST.get('email','')
    if User.objects.filter(email__iexact=email) or User.objects.filter(usermembership__paypal_email__iexact=email):
      m = "An account with that email address already exists. "
      m += "Please use the form below to reset your password. "
      m += "If you believe this is in error, please email chris [{at}] lablackey.com"
      messages.error(request,m)
      return HttpResponseRedirect(reverse('password_reset'))
  return _register(request,'registration.backends.default.DefaultBackend',*args,**kwargs)

@limited_login_required
def unsubscribe(request,attr,user_id):
  if not str(request.limited_user.id) == user_id:
    return FORBIDDEN
  usermembership = request.limited_user.usermembership
  setattr(usermembership,"notify_"+attr,False)
  usermembership.save()
  return TemplateResponse(request,'membership/unsubscribe.html',{'attr':attr})

def roland_email(request,y=2012,m=1,d=1):
  if not request.user.is_superuser:
    raise Http404
  import csv
  dt = datetime.date(int(y),int(m),int(d))
  # Create the HttpResponse object with the appropriate CSV header.
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="txrx_emails_%s-%s-%s.csv"'%(y,m,d)

  writer = csv.writer(response)
  for user in User.objects.filter(date_joined__gt=dt,is_active=True):
    writer.writerow([user.email,user.username,str(user.date_joined)])

  return response

def officers(request):
  officers = Officer.objects.all()
  values = {'officers': officers}
  return TemplateResponse(request,'membership/officers.html',values)

def verify_api(request):
  if not getattr(settings,'PORTAL_KEY','') == request.REQUEST.get('api_key',''):
    raise Http404

def user_emails(request):
  verify_api(request)
  out = []
  for u in User.objects.all():
    out.append(','.join([str(u.id),u.email or '',u.usermembership.paypal_email or '']))
  return HttpResponse('\n'.join(out))

def course_names(request):
  verify_api(request)
  out = []
  for c in Course.objects.all():
    out.append(','.join([str(c.id),c.name]))
  return HttpResponse('\n'.join(out))

def course_completion(request,year=None,month=None,day=None):
  verify_api(request)
  out = []
  if year:
    dt = datetime.date(int(year),int(month),int(day))
  else:
    dt = datetime.date.today()-datetime.timedelta(30)
  completions = CourseCompletion.objects.filter(created__gte=dt)
  if 'course_id' in request.GET:
    completions = completions.filter(course_id=request.GET['course_id'])
  for c in completions:
    out.append(','.join([str(c.course.id),str(c.user.id)]))
  return HttpResponse('\n'.join(out))
