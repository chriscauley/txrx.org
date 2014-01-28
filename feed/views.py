from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404

from .models import Thing

def thing_detail(request,pk,slug):
  thing = get_object_or_404(Thing,pk=pk)
  values = {
    'thing': thing,
  }
  return TemplateResponse(request,'feed/thing_detail.html',values)
