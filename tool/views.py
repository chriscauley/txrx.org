from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from tool.models import Tool, Lab, Permission, Group

import json

def lab_index(request):
  values = {'labs': Lab.objects.all()}
  return TemplateResponse(request,'tool/lab_index.html',values)

def lab_detail(request,lab_slug,pk):
  values = {'lab': get_object_or_404(Lab,pk=pk) }
  return TemplateResponse(request,'tool/lab_detail.html',values)

def tool_detail(request,tool_slug,pk):
  tool = get_object_or_404(Tool,pk=pk)
  values = {
    'tool': tool,
    'lab': tool.lab,
  }
  return TemplateResponse(request,'tool/tool_detail.html',values)

@login_required
def my_permissions(request):
  columns = [{'rows':[]},{'rows':[]}]
  for group in Group.objects.all():
    g = {
      'id': group.id,
      'color': group.color,
      'permissions': [],
    }
    for permission in group.permission_set.all():
      g['permissions'].append(permission.as_json)
    columns[group.column]['rows'].append(g)
  values = {
    'columns': json.dumps(columns)
  }
  return TemplateResponse(request,'criterion/my_permissions.html',values)

@staff_member_required
def criterion_index(request):
  permissions = Permission.objects.all()
  values = {
    'permission_criteria_tuples': [(p,p.get_criteria_can_grant(request.user)) for p in permissions]
  }
  return TemplateResponse(request,'criterion/index.html',values)
