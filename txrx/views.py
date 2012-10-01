from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.conf import settings
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from articles.models import Article
from django.shortcuts import get_object_or_404
from project.models import Project
from membership.models import Membership, Profile
from tool.models import Tool, Lab

import os,urllib, re

RC = lambda r: dict(context_instance=RequestContext(r))
_models = {"article": Article,
           "project": Project}

def jsonable(f):
    def wrap(request,*args,**kwargs):
        from copy import copy
        request = copy(request)
        request.TEMPLATE="base.html"
        if request.path.endswith(".json"):
            request.TEMPLATE="json"
        return f(request,*args,**kwargs)
    wrap.__doc__ = f.__doc__; wrap.__name__ = f.__name__
    return wrap

@jsonable
def home(request):
    values = {'feed': Article.objects.live()[:10]}
    return render_to_response("feed.html",values, **RC(request))

@jsonable
def comming_soon(request):
    return render_to_response("comming_soon.html",{},**RC(request))

@jsonable
def generic(request,name):
    values = {'memberships':Membership.objects.active()}
    return TemplateResponse(request,name+".html",values)

def feed(request,model):
    model = _models[model]
    values = {'feed': model.objects.live()[:10]}
    return TemplateResponse(request,"feed.html",values)

def item(request,model,year,slug):
    """Displays a single item."""
    model = _models[model]

    try:
        item = model.objects.live(user=request.user).get(publish_date__year=year, slug=slug)
    except Article.DoesNotExist:
        raise Http404
    values = {'item':item}
    return TemplateResponse(request,"item.html",values)

@jsonable
def tools(request,lab=None,tool=None):
    labs = Lab.objects.all()
    if tool:
        tool = get_object_or_404(Tool,slug=tool)
        lab = tool.lab
    if lab:
        lab = get_object_or_404(Lab,slug=lab)
    values = {
        "labs": labs,
        "current_lab": lab,
        "current_tool": tool,
        }
    return TemplateResponse(request,"tools.html",values)

def projects(request,slug=None):
    values = {"feed": Project.objects.all(),
              }
    return TemplateResponse(request,"feed.html",values)

def members(request,username=None):
    memberships = Membership.objects.active()[::-1]
    values = {'memberships':memberships}
    return TemplateResponse(request,"members.html",values)

def member(request,username=None):
    member = User.objects.get(username=username)
    values = {'member':member}
    return TemplateResponse(request,"member.html",values)

def google_login (request):
    from google_login import GoogleLogin
    #ocsession = Session(request)
    url = settings.ROOT_URL+request.REQUEST.get('next','home').lstrip("/")
     
    ret_url = settings.ROOT_URL + 'google_return/' + urllib.quote(url)

    g = GoogleLogin()
     
    return HttpResponseRedirect(g.get_login_url(ret_url))
     
def google_return (request, url=None):
    from django.contrib.auth import login
    good = False
    # ocdir.clean_gkeys()
     
    email = request.REQUEST.get('openid.ext1.value.email', '')
    handle = request.REQUEST.get('openid.assoc_handle', '')
    mode = request.REQUEST.get('openid.mode', '')
    if handle != '' and email != '' and mode == 'id_res':
        u = User.objects.filter(email=email)
        if not u:
            u = User(email=email,username=email.split("@")[0])
            u.save()
            u.set_unusable_password()
        u = User.objects.get(email=email)
        u.backend='django.contrib.auth.backends.ModelBackend'
        login(request,u)
        good = True
        x = request.user

    if not url.startswith("http://"):
        url = url.replace("http:/", "http://")

    if not re.search("http://", url):
        url = "http://" + url

    if good:
        return HttpResponseRedirect(url)
    if not "?" in url:
        url += "?"
    url += '&message='
    url += urllib.quote("Invalid Google login, please try again.")

    return HttpResponseRedirect(url)

@login_required
def survey(request):
    from membership.models import Survey
    from membership.forms import SurveyForm
    form = SurveyForm(request.POST)
    values = {"form": form}
    if request.method == "POST":
        pass
    return TemplateResponse(request,"survey.html",values)
