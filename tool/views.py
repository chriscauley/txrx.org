from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from tool.models import Tool, Lab, Permission

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

@staff_member_required
def criterion_index(request):
  permissions = Permission.objects.all()
  values = {
    'permission_criteria_tuples': [(p,p.get_criteria_can_grant(request.user)) for p in permissions]
  }
  return TemplateResponse(request,'criterion/index.html',values)
