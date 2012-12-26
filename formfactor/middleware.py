from django.conf import settings
from django.template.response import TemplateResponse

from .user_agents import SEARCH_STRINGS

FORCE_FORM_FACTOR = getattr(settings, 'FORCE_FORM_FACTOR', None)

class FormFactor (object):
  def process_response(self,request,response):
    if getattr(request,'form_factor',None):
      response.set_cookie('FORM_FACTOR',request.form_factor)
    return response

  def process_template_response (self, request, response):
    response.set_cookie('FORM_FACTOR',request.form_factor)
    if request.form_factor == 'mobile' or request.form_factor == 'tablet':
      if isinstance(response, TemplateResponse):
        if hasattr(response, 'template_name'):
          t = response.template_name
          n = t.split('/')
          if request.form_factor == 'mobile':
            n.insert(-1,"mobile")
          else:
            n.insert(-1,"tablet")
          n = "/".join(n)

          response.template_name = [n,t]

    return response
    
  def process_request (self, request):
    fff = request.REQUEST.get('fff', '')
    request.form_factor = 'desktop'

    if FORCE_FORM_FACTOR:
      request.form_factor = FORCE_FORM_FACTOR
      
    elif fff:
      request.form_factor = fff
    else:
      cookie_value = request.COOKIES.get('FORM_FACTOR', '')
      if cookie_value:
        request.form_factor = cookie_value
        
      else:
        if request.META.has_key("HTTP_X_OPERAMINI_FEATURES"):
          request.form_factor = 'mobile'
          
        if request.form_factor == 'desktop' and request.META.has_key("HTTP_ACCEPT"):
          s = request.META["HTTP_ACCEPT"].lower()
          if 'application/vnd.wap.xhtml+xml' in s:
            request.form_factor = 'mobile'
            
        if request.form_factor == 'desktop' and request.META.has_key("HTTP_USER_AGENT"):
          s = request.META["HTTP_USER_AGENT"].lower()
          for ua in SEARCH_STRINGS:
            if ua in s:
              request.form_factor = 'mobile'
              
        if request.form_factor == 'mobile' and request.META.has_key("HTTP_USER_AGENT"):
          if 'ipad' in request.META['HTTP_USER_AGENT'].lower() or 'android 3' in request.META['HTTP_USER_AGENT'].lower():
            request.form_factor = 'tablet'
