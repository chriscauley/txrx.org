from django.conf.urls.defaults import *

urlpatterns = patterns(
  'membership.views',
  url(r'^$','join_us'),
  url(r'^officers/$', 'officers', name='officers'),
  url(r'^minutes/(\d+-\d+-\d+)/$', 'minutes', name='meeting_minutes',),
  url(r'^unsubscribe/(global|comments|classes)/(?P<user_id>\d+)/$', 'unsubscribe', name='unsubscribe'),
  url(r'^notify_course/(\d+)/$','notify_course',name='notify_course'),
  url(r'^clear_notification/(notify_course)/(\d+)/(\d+)$','clear_notification',name='clear_notification'),
)
