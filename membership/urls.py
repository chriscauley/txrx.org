from django.conf.urls.defaults import *

urlpatterns = patterns(
  'membership.views',
  url(r'^redirect/$', 'login_redirect', name='membership.redirector',),
  url(r'^minutes/(\d+-\d+-\d+)/$', 'minutes', name='meeting_minutes',),
  )
