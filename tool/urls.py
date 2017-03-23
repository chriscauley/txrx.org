from django.conf.urls import patterns, url

import views

urlpatterns = [
  url(r'^$', views.lab_index,name='lab_index'),
  url(r'^lab/([^/]+)_(\d+)/$', views.lab_detail,name='lab_detail'),
  url(r'^([^/]+)_(\d+)/$', views.tool_detail,name='tool_detail'),
  url(r'^toggle_criterion/$', views.toggle_criterion),
  url(r'^master/(\w+)/(\w+)/$', views.master, name="tool_master"),
]
