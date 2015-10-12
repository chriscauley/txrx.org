from django.conf.urls import patterns, url

urlpatterns = patterns(
  'tool.views',
  url(r'^$','lab_index',name='lab_index'),
  url(r'^lab/([^/]+)_(\d+)/$','lab_detail',name='lab_detail'),
  url(r'^my-permissions/$', 'my_permissions', name="my_permissions"),
  url(r'^([^/]+)_(\d+)/$','tool_detail',name='tool_detail'),
  )
