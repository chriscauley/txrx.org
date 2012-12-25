from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.models import User
from django.conf import settings
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from membership.models import Membership
from codrspace.models import Post

def members(request,username=None):
    memberships = Membership.objects.active()[::-1]
    values = {'memberships':memberships}
    return TemplateResponse(request,"members.html",values)

def member(request,username=None):
    member = User.objects.get(username=username)
    values = {'member':member}
    return TemplateResponse(request,"member.html",values)

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
    u = User.objects.get(id=uid)
    from django.contrib.auth import login
    u.backend='django.contrib.auth.backends.ModelBackend'
    login(request,u)
    return HttpResponseRedirect('/')

def blog_home(request):
    posts = Post.objects.filter(status="published",featured=False)[:10]
    featured_posts = Post.objects.filter(status="published",featured=True)
    values = {
        'posts': posts,
        'featured_posts': featured_posts,
        }
    return TemplateResponse(request,"blog_home.html",values)
