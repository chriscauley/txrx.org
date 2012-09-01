from django.conf.urls.defaults import *

urlpatterns = patterns(
  'course.views',
  (r'^$', 'index'),
  url(r'^instructor/([^/]+)/$', 'instructor_detail',name='instructor_detail'),
)
