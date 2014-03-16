from django.template.response import TemplateResponse

from django.shortcuts import get_object_or_404

from tool.models import Tool, Lab

def lab_index(request):
  values = {'labs': Lab.objects.all()}
  return TemplateResponse(request,'tool/lab_index.html',values)

def lab_detail(request,lab_slug):
  values = {'lab': get_object_or_404(Lab,slug=lab_slug)}
  return TemplateResponse(request,'tool/lab_detail.html',values)

def tool_detail(request,lab_slug,tool_slug):
  tool = get_object_or_404(Tool,slug=tool_slug)
  values = {
    'tool': tool,
    'lab': tool.lab,
  }
  return TemplateResponse(requset,'tool/tool_detail.html',values)
