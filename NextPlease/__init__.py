from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django import http
from django.template.response import TemplateResponse

PER_PAGE = getattr(settings, 'PER_PAGE', 10)

class NextPleasePaginator (Paginator):
  def __init__ (self, request, object_list, per_page, page_param='page', orphans=0, allow_empty_first_page=True):
    self.request = request
    self.page_param = page_param
    
    super().__init__ (object_list, per_page, orphans=orphans, allow_empty_first_page=allow_empty_first_page)
    
  def current (self):
    if not hasattr(self, '_current'):
      data = self.request.POST or self.request.GET
      page = data.get(self.page_param, '1')
      
      try:
        self._current = self.page(page)
        
      except PageNotAnInteger:
        raise http.Http404
        
      except EmptyPage:
        raise http.Http404
        
    return self._current
    
  def current_list (self):
    return self.current().object_list
    
  def number (self):
    return self.current().number
    
  def has_previous (self):
    return self.current().has_previous()
    
  def has_next (self):
    return self.current().has_next()
    
  def previous_qs (self):
    qs = self.request.META['QUERY_STRING']
    cs = '%s=%d' % (self.page_param, self.number())
    if self.has_previous():
      ps = '%s=%d' % (self.page_param, self.number() - 1)
      if qs:
        if cs in qs:
          qs = qs.replace(cs, ps)
          
        else:
          qs = qs + '&' + ps
          
      else:
        qs = ps
        
    return qs
    
  def next_qs (self):
    qs = self.request.META['QUERY_STRING']
    cs = '%s=%d' % (self.page_param, self.number())
    if self.has_next():
      ps = '%s=%d' % (self.page_param, self.number() + 1)
      
      if qs:
        if cs in qs:
          qs = qs.replace(cs, ps)
          
        else:
          qs = qs + '&' + ps
          
      else:
        qs = ps
        
    return qs
    
def pagination (object_list_var, per_page=PER_PAGE, page_param='page', output_var='paginator', orphans=0, allow_empty_first_page=True, request_arg=0):
  def decorator(target):
    def wrapper(*args, **kwargs):
      tpl_response = target(*args, **kwargs)
      if isinstance(tpl_response,TemplateResponse):
        tpl_response.context_data[output_var] = NextPleasePaginator(
          args[request_arg],
          tpl_response.context_data[object_list_var],
          per_page,
          page_param,
          orphans,
          allow_empty_first_page
          )

      return tpl_response
      
    return wrapper
    
  return decorator
  
