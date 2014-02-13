from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404

from .models import Thing

from NextPlease import pagination

@pagination("things",per_page=36)
def thing_index(request):
  things = Thing.objects.filter(active=True)
  values = {
    'things': things,
  }
  return TemplateResponse(request,'thing/index.html',values)

def thing_detail(request,pk,slug):
  thing = get_object_or_404(Thing,pk=pk,active=True)
  values = {
    'thing': thing,
  }
  return TemplateResponse(request,'thing/detail.html',values)
