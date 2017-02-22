from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from course.models import Course
from membership.utils import limited_login_required
from .models import Follow

from lablackey.contenttypes import get_contenttype
from lablackey.utils import FORBIDDEN

@limited_login_required
def unsubscribe(request,attr,user_id):
  if not str(request.limited_user.id) == user_id:
    return FORBIDDEN
  if attr == 'notify_course':
    Follow.objects.filter(user=request.limited_user).delete()
  else:
    usermembership = request.limited_user.usermembership
    setattr(usermembership,"notify_"+attr,False)
    usermembership.save()
  return TemplateResponse(request,'notify/unsubscribe.html',{'attr':attr})

@limited_login_required
def unfollow(request,follow_id):
  follow = get_object_or_404(Follow,id=follow_id)
  if follow.user_id != request.limited_user.id:
    return FORBIDDEN
  obj = follow.content_object
  messages.success(request,"You are no longer following: {follow.content_object}".format(follow=follow))
  follow.delete()
  return HttpResponseRedirect(request.GET.get("next",obj.get_absolute_url()))

@login_required
def follow(request,contenttype,id):
  contenttype = get_contenttype(contenttype)
  follow, new = Follow.objects.get_or_create(user=request.user,content_type=contenttype,object_id=id)
  messages.success(request,"You are now following: {follow.content_object}".format(follow=follow))
  return HttpResponseRedirect(request.GET.get("next",follow.content_object.get_absolute_url()))
