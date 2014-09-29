from django.contrib.contenttypes.models import ContentType
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404

from .models import Thing, Material
from tool.models import Tool, TaggedTool

from NextPlease import pagination

filters = {
  "material": lambda: {
    "model": Material,
    "options": Material.objects.all(),
    "name": "Material",
    "slug": "material",
  },
  "tool": lambda: {
    "model": Tool,
    "options": Tool.objects.all(),
    "name": "Tool",
    "slug": "tool",
  }
}

@pagination("things",per_page=36)
def thing_index(request):
  things = Thing.objects.filter(active=True)
  #tool_filter = filters['tool']()
  #contenttype = ContentType.objects.get(name="thing")
  #for tool in tool_filter['options']:
  #  tool.count = TaggedTool.objects.filter(tool_id=tool.id,content_type=contenttype).count()
  #tool_filter['options'] = [t for t in tool_filter['options'] if t.count > 1]
  if "material" in request.GET:
    things = things.filter(materials__pk=request.GET['material'])
  if "tool" in request.GET:
    things = things.filter(tools__pk=request.GET['tool'])
  values = {
    'things': things,
    'filters': [filters['material']()],
  }
  return TemplateResponse(request,'thing/index.html',values)

def thing_detail(request,pk,slug):
  thing = get_object_or_404(Thing,pk=pk,active=True)
  values = {
    'thing': thing,
  }
  return TemplateResponse(request,'thing/detail.html',values)
