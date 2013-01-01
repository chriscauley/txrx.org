from django.template.response import TemplateResponse

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
    values['current_lab'] = labs.get(slug=lab_slug)
    template = 'lab_detail'
  if tool_slug:
    values['current_tool'] = Tool.objects.get(slug=tool_slug)
    template = 'tool_detail'
  return TemplateResponse(request,'tool/%s.html'%template,values)

