from django.conf.urls.defaults import *

urlpatterns = patterns(
  'course.views',
  (r'^$', 'index'),
  (r'^term/(\d+)/', 'index'),
  url(r'^instructor/([^/]+)/$', 'instructor_detail',name='instructor_detail'),
  url(r'^my-sessions/$', 'my_sessions',name='my_sessions'),
  url(r'^all-sessions/$', 'all_sessions',name='all_sessions'),
  url(r'^evaluations/$','evaluation_index',name='evaluation_index'),
  url(r'^evaluation/(\d+)/$','evaluation_detail',name='evaluation_detail'),
  url(r'^totals/$','course_totals',name='course_totals'),
  url(r'^([\w\d\-\_]+)/$','detail',name='detail'),
  url(r'^debug/(?P<id>\d+)/$', 'debug_parsing',name='debug_parsing'),
  url(r'^email/instructor/(\d+)/$','email_instructor',name='email_instructor'),
  url(r'^ics/(all_classes).ics$','ics_classes_all',name='ics_classes_all'),
)
