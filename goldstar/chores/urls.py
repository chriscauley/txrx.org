from django.conf.urls.defaults import patterns, include, url
import os
urlpatterns = patterns(
  'chores.views',
  url(r'^assign/(\d+)/$', "assign", name="assign"),
  url(r'^complete/(\d+)/$', "complete", name="complete"),
)
