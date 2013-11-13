from django.template.response import TemplateResponse

from django.shortcuts import get_object_or_404

from tool.models import Tool, Lab

def tools(request,lab_slug=None,tool_slug=None):
  """
  One View to Rule them All!
  The presence of slugs changes the templates and populates values dict.
  """
  labs = Lab.objects.all()
  template = 'lab_index'
  values = { 'labs': labs, }
  if lab_slug:
    values['current_lab'] = get_object_or_404(Lab,slug=lab_slug)
    template = 'lab_detail'
  if tool_slug:
    values['current_tool'] = get_object_or_404(Tool,slug=tool_slug)
    template = 'tool_detail'
  return TemplateResponse(request,'tool/%s.html'%template,values)

