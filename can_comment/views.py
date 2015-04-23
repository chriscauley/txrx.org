#! in 1.7+ use from django.contrib.sites.shortcuts import get_current_site
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import get_current_site
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.template.defaultfilters import date
from mptt_comments.models import MpttComment

import json, string

def ajax_login_required(function):
  def wrap(request,*args,**kwargs):
    if not request.user.is_authenticated():
      print request.user
      response = HttpResponse("Unauthorized: You must be logged in to do that.")
      response.status_code = 401
      return response
    return function(request,*args,**kwargs)
  wrap.csrf_exempt = True
  return wrap

def test(request):
  values = {
    'comments': MpttComment.objects.all().count()
  }
  return TemplateResponse(request,'ct.html',values)

def make_branch(a,level):
  return {
    'letter': a,
    'extras': [make_branch(l,level-1) for l in string.digits[:2] if level > 0],
  }

def build_comment_json(comment):
  return {
    'pk': comment.pk,
    'children': [build_comment_json(c) for c in comment.get_children()],
    'username': comment.user.username,
    'user_pk': comment.user_id,
    'date_s': date(comment.submit_date,"l F j, Y @ P").replace("@","at"),
    'content': comment.comment,
  }

def list_comments(request):
  natural_key = request.GET.get('content_type').split('.')
  comments = MpttComment.objects.filter(
    object_pk=request.GET['object_pk'],
    content_type=ContentType.objects.get_by_natural_key(*natural_key),
    parent=None
  ).order_by("-submit_date") # this should eventually be on MpttComment.Meta
  comments_json = [build_comment_json(c) for c in comments]
  return HttpResponse(json.dumps(comments_json))

#! TODO most of this function should be a shared form with edit
@ajax_login_required
def post(request):
  parent_pk = request.POST.get("parent_pk",None)
  if parent_pk:
    parent = get_object_or_404(MpttComment,pk=parent_pk)
    content_type = parent.content_type
    object_pk = parent.object_pk
  else:
    parent = None
    natural_key = request.POST.get('content_type').split('.')
    content_type = ContentType.objects.get_by_natural_key(*natural_key)
    object_pk = request.POST.get('object_pk')
  comment = MpttComment.objects.create(
    user=request.user,
    content_type=content_type,
    object_pk=object_pk,
    parent=parent,
    comment=request.POST.get('comment'),
    site=get_current_site(request),
    ip_address=request.META.get("REMOTE_ADDR", None),
  )
  return HttpResponse(json.dumps(build_comment_json(comment)))

#! TODO not implimented

@ajax_login_required
def edit(request,pk):
  comment = get_object_or_deny(MpttComment,user,pk=pk)
  return HttpResponse(json.dumps(build_comment_json(comment)))

def get_object_or_deny(model,user_object,*args,**kwargs):
  obj = get_object_or_404(model,*args,**kwargs)
  if not (request.user.is_superuser or request.user == obj.user):
    raise PermissionDenied()
  return obj

#! TODO Not implimented
@ajax_login_required
def delete(request,pk):
  comment = get_object_or_deny(MpttComment,user,pk=pk)
  comment.is_removed = True
  comment.save()
  HttpResponse("You have deleted this Comment.")

#! TODO Not implimented
@ajax_login_required
def flag(request,pk):
  comment = get_object_or_deny(MpttComment,user,pk=pk)
  comment.is_flagged = True
  comment.save()
  HttpResponse("This comment has been flagged and will be reviewed.")
