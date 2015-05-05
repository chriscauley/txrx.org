from django.conf.urls import patterns, include, url
import os
urlpatterns = patterns(
  'chore.views',
  url(r'^$','index',name='index'),
  url(r'^assign/(\d+)/$', "assign", name="assign"),
  url(r'^complete/(\d+)/$', "complete", name="complete"),
)
