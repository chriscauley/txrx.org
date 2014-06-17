from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from ..models import Session
from ..forms import EmailInstructorForm
from membership.models import UserMembership
from thing.models import Thing
from codrspace.models import Post

def index(request,username=None):
  instructors = UserMembership.objects.list_instructors()
  values = {'instructors':instructors}
  return TemplateResponse(request,"course/instructors.html",values)

def detail(request,username=None):
  profile = get_object_or_404(UserMembership,user__username=username)
  things = Thing.objects.filter(user=profile.user,active=True)
  posts = Post.objects.filter(user=profile.user, status = 'published').order_by("-publish_dt")
  values = {
    'thing_header': profile.user.username + "'s Things",
    'post_header' : profile.user.username + "'s Blog Posts",
    'profile': profile,
    'things': things,
    'posts': posts
    }
  return TemplateResponse(request,"course/instructor_detail.html",values)

def email(request,session_pk):
  session = get_object_or_404(Session,pk=session_pk)
  form = EmailInstructorForm(session,request)
  if request.POST and form.is_valid():
    form.send()
  values = {'form': form}
  return TemplateResponse(request,"course/email_instructor.html",values)
