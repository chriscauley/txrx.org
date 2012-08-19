from django.conf.urls.defaults import *

urlpatterns = patterns(
  'course.views',
  (r'^$', 'index'),
)
