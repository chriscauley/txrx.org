from django.conf.urls.defaults import *

urlpatterns = patterns(
  'membership.views',
  url(r'^$','join_us'),
  url(r'^officers/$', 'officers', name='officers'),
  url(r'^minutes/(\d+-\d+-\d+)/$', 'minutes', name='meeting_minutes',),
  url(r'^unsubscribe/(global|comments|classes)/(?P<user_id>\d+)/$', 'unsubscribe', name='unsubscribe'),
  )
