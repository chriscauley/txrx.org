from django.conf import settings
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

default_theme = getattr(settings,"DEFAULT_THEME","default")

class Theme(object):
  def process_response(self,request,response):
    if getattr(request,'theme',None):
      try:
        response.set_cookie('THEME',request.theme)
      except UnicodeEncodeError:
        pass
    return response

  def process_template_response (self, request, response):
    try:
      response.set_cookie('THEME',request.theme)
    except UnicodeEncodeError:
      pass
    return response
    
  def process_request (self, request):
    cookie_value = request.COOKIES.get('THEME', '')
    request.theme = request.GET.get('set_theme',None) or cookie_value or default_theme
    if 'set_theme' in request.GET:
      return HttpResponseRedirect(request.path)
