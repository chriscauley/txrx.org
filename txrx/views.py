from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, HttpResponse, Http404

from blog.models import Post, Banner
from membership.models import Membership
from thing.models import Thing

from NextPlease import pagination
from tagging.models import Tag
import random, datetime

@login_required
def survey(request):
  from membership.models import Survey
  from membership.forms import SurveyForm
  form = SurveyForm(request.POST)
  values = {"form": form}
  if request.method == "POST":
    pass
  return TemplateResponse(request,"survey.html",values)

@login_required
def force_login(request,uid):
  if not request.user.is_superuser:
    raise Http404()
  u = get_object_or_404(get_user_model(),pk=uid)
  from django.contrib.auth import login
  u.backend='django.contrib.auth.backends.ModelBackend'
  login(request,u)
  return HttpResponseRedirect('/')

def index(request):
  posts = Post.objects.filter(status="published",publish_dt__lte=datetime.datetime.now())
  things = list(Thing.objects.filter(featured=True)[:20])
  values = {
    'things': random.sample(things,min(len(things),8)),
    'posts': posts[:5],
    'banner': Banner.objects.get_random(),
    }
  return TemplateResponse(request,"index.html",values)

@pagination("posts")
def blog_home(request):
  posts = Post.objects.filter(status="published",publish_dt__lte=datetime.datetime.now())
  _t = Tag.objects.cloud_for_model(Post)
  tags = sorted([(t,t.count) for t in _t if t.count > 1],key=lambda t:-t[1])
  values = {
    "posts": posts,
    "post_tags": tags,
    }
  return TemplateResponse(request,"blog/home.html",values)

def intentional_500(request):
  arst

def to_template(request,template_name):
  return TemplateResponse(request,"flatpages/{}.html".format(template_name),{})
