from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.template.defaultfilters import date
from mptt_comments.models import MpttComment

import json, string

def index(request):
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
  x = dir(comment)
  return {
    'pk': comment.pk,
    'children': [build_comment_json(c) for c in comment.get_children()],
    'username': comment.user.username,
    'user_pk': comment.user_id,
    'date_s': date(comment.submit_date,"l F j, Y @ P").replace("@","at"),
    'content': comment.comment,
  }

def can_comments(request):
  comments = MpttComment.objects.filter(
    object_pk=request.GET['object_pk'],
    content_type__app_label=request.GET['app'],
    content_type__name=request.GET['name'],
    parent=None
  )
  comments_json = [build_comment_json(c) for c in comments]
  return HttpResponse(json.dumps(comments_json))
