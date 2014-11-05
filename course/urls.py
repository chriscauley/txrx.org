from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns(
  'course.views',
  url(r'^email/instructor/(\d+)/$','instructor.email',name='email_instructor'),

  url(r'^evaluations/$','evaluation.index',name='evaluation_index'),
  url(r'^evaluation/(\d+)/$','evaluation.detail',name='evaluation_detail'),
  url(r'^refuse_evaluation/(\d+)/$','evaluation.refuse',name='evaluation_refuse'),
  url(r'^instructor_evaluations/(\d+)/$','evaluation.instructor_detail',name='instructor_evaluations'),
  url(r'^debug/(?P<id>\d+)/$', 'debug_parsing',name='debug_parsing'),

  url(r'^$', 'classes.index'),
  url(r'^rsvp/(\d+)/','classes.rsvp',name='rsvp'),
  url(r'^term/(\d+)/', 'classes.index'),
  url(r'^ics/(all_classes).ics$','classes.ics_classes_all',name='ics_classes_all'),
  url(r'^ics/(\d+)/([^/]+)/(my-classes).ics$','classes.ics_classes_user',name='ics_classes_user'),
  url(r'^totals/$','classes.course_totals',name='course_totals'),
  url(r'^full/$','classes.course_full',name='course_full'),
  url(r'^start_checkout/$','classes.start_checkout',name='start_checkout'),
  url(r'^delay_reschedule/(\d+)/(\d|close)/$', 'classes.delay_reschedule',name='delay_reschedule'),
  url(r'^([\w\d\-\_]+)/$','classes.detail',name='detail'),
)
