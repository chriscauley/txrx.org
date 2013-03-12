from django.conf.urls.defaults import *

urlpatterns = patterns(
  'course.views',
  (r'^$', 'index'),
  (r'^term/(\d+)/', 'index'),
  url(r'^instructor/([^/]+)/$', 'instructor_detail',name='instructor_detail'),
  url(r'^my-sessions/$', 'my_sessions',name='my_sessions'),
  url(r'^all-sessions/$', 'all_sessions',name='all_sessions'),
  url(r'^([\w\d\-\_]+)/$','detail',name='detail'),
  url(r'^debug/(?P<id>\d+)/$', 'debug_parsing',name='debug_parsing'),
  url(r'^email/instructor/(\d+)/$','email_instructor',name='email_instructor'),
)
