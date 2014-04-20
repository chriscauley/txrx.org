from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.template.response import TemplateResponse

redirect = lambda request,url: HttpResponseRedirect(url)
predirect = lambda request,url: HttpResponsePermanentRedirect(url)

def gfycat(request):
  return TemplateResponse(request,"gfycat.html",{'slug':request.GET.get('url').split('/')[-1]})
