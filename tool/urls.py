from django.conf.urls.defaults import *

urlpatterns = patterns(
  'tool.views',
  url(r'^$','lab_index',name='lab_index'),
  url(r'^([^/]+)/$','lab_detail',name='lab_detail'),
  url(r'^([^/]+)/([^/]+)/$','tool_detail',name='tool_detail'),
  )
