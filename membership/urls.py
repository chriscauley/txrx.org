from django.conf.urls.defaults import *

urlpatterns = patterns(
  'membership.views',
  url(r'^$','join_us'),
  url(r'^minutes/(\d+-\d+-\d+)/$', 'minutes', name='meeting_minutes',),
  url(r'^unsubscribe/([\w\d]+)/$', 'unsubscribe', name='unsubscribe'),
  url(r'^unsubscribe_comments/([\d]+)/$', 'unsubscribe_comments', name='unsubscribe_comments'),
  )
