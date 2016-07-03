from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponse, Http404

from blog.models import Post, Banner
from thing.models import Thing

from tagging.models import Tag
import random, datetime

redirect = lambda request,url: HttpResponseRedirect(url)
predirect = lambda request,url: HttpResponsePermanentRedirect(url)

def beta(request,page_name=None):
  is_kiosk = request.path in ["/checkin/"]
  values = {
    'BODY_CLASS': "kiosk" if is_kiosk else "",
    'REDESIGNED': is_kiosk
  }
  return TemplateResponse(request,"beta.html",values)

def gfycat(request):
  return TemplateResponse(request,"gfycat.html",{'slug':request.GET.get('url').split('/')[-1]})

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

def intentional_500(request):
  arst

def to_template(request,template_name):
  return TemplateResponse(request,"flatpages/{}.html".format(template_name),{})
