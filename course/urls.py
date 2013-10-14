from django.conf.urls.defaults import *

urlpatterns = patterns(
  'course.views',
  url(r'^my-sessions/$', 'my_sessions',name='my_sessions'),
  url(r'^all-sessions/$', 'all_sessions',name='all_sessions'),
  url(r'^instructor/([^/]+)/$', 'instructor.detail',name='instructor_detail'),
  url(r'^email/instructor/(\d+)/$','instructor.email',name='email_instructor'),

  url(r'^evaluations/$','evaluation.index',name='evaluation_index'),
  url(r'^evaluation/(\d+)/$','evaluation.detail',name='evaluation_detail'),
  url(r'^instructor_evaluations/(\d+)/$','evaluation.instructor_detail',name='instructor_evaluations'),
  url(r'^debug/(?P<id>\d+)/$', 'debug_parsing',name='debug_parsing'),

  (r'^$', 'classes.index'),
  (r'^term/(\d+)/', 'classes.index'),
  url(r'^ics/(all_classes).ics$','classes.ics_classes_all',name='ics_classes_all'),
  url(r'^totals/$','classes.course_totals',name='course_totals'),
  url(r'^([\w\d\-\_]+)/$','classes.detail',name='detail'),
)
