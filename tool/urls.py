from django.urls import path, re_path

from . import views

urlpatterns = [
  path('', views.lab_index,name='lab_index'),
  re_path(r'^lab/([^/]+)_(\d+)/$', views.lab_detail,name='lab_detail'),
  re_path(r'^([^/]+)_(\d+)/$', views.tool_detail,name='tool_detail'),
  path('toggle_criterion/', views.toggle_criterion),
  re_path(r'^master/(\w+)/(\w+)/$', views.master, name="tool_master"),
]
