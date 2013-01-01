from django.conf.urls.defaults import *

urlpatterns = patterns(
  'tool.views',
  url(r'^$','tools',name='lab_index'),
  url(r'^([^/]+)/$','tools',name='lab_detail'),
  url(r'^([^/]+)/([^/]+)/$','tools',name='tool_detail'),
  )
