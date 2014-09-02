from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from .models import Membership, MembershipGroup, MeetingMinutes, Officer, UserMembership
from .forms import UserForm, UserMembershipForm, RegistrationForm
from .utils import limited_login_required, verify_unique_email

from codrspace.models import Post
from course.models import Course,CourseCompletion, Session
from thing.models import Thing
from txrx.utils import FORBIDDEN

import datetime

def join_us(request):
  values = {
    'groups': MembershipGroup.objects.all(),
    'flatpage':lambda:FlatPage.objects.get(url='/join-us/'),
    }
  return TemplateResponse(request,"membership/memberships.html",values)

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
    'notify_courses': user.notifycourse_set.all(),
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
  email = request.POST.get('email','')
  m = "Please use the form below to reset your password. "
  m += "<br />If you believe this is in error, please email %s"%settings.CONTACT_LINK
  if request.POST and not verify_unique_email(email):
    m = "An account with the email address %s already exists. %s"%(email,m)
    messages.error(request,m,extra_tags='danger')
    return HttpResponseRedirect(reverse('password_reset'))
  paypal_email = request.POST.get('paypal_email','')
  if request.POST and not verify_unique_email(paypal_email):
    m = "An account with the paypal email address %s already exists. "%(paypal_email,m)
    messages.error(request,m,extra_tags='danger')
    return HttpResponseRedirect(reverse('password_reset'))
  form = RegistrationForm(request.POST or None)
  if form.is_valid():
    user = form.save(request)
    return HttpResponseRedirect(reverse('registration_complete'))
  values = {
    'form': form,
  }
  return TemplateResponse(request,'registration/registration_form.html',values)

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

def member_index(request,username=None):
  instructors = UserMembership.objects.list_instructors()
  values = { 'instructors': instructors }
  return TemplateResponse(request,"membership/member_index.html",values)

def member_detail(request,username=None):
  user = get_object_or_404(User,username=username)
  things = Thing.objects.filter(user=user,active=True)
  posts = Post.objects.filter(user=user, status = 'published').order_by("-publish_dt")
  values = {
    'thing_header': user.username + "'s Things",
    'post_header' : user.username + "'s Blog Posts",
    'user': user,
    'profile': user.usermembership,
    'things': things,
    'posts': posts
    }
  return TemplateResponse(request,"membership/member_detail.html",values)
