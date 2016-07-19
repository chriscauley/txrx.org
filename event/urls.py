from django.conf.urls import *

urlpatterns = patterns(
  'event.views',
  url(r'^$', 'index', name="index"),
  url(r'^(\d+\-\d+\-\d+)/$', 'index', name="index"),
  url(r'^occurrence/(\d+)/$','occurrence_detail',name='occurrence_detail'),
  url(r'^(\d+)/(.+)/$','occurrence_detail',name='occurrence_detail'),
  url(r'ics/([^/]+)/([^/]+)/(\d+)/(.+).ics','ics',name="ics"),
  url(r'ics/(all_events).ics','all_ics',name="all_ics"),
  url(r'eventdetail_(\d+).json','detail_json'),
  #url(r'weekly/(\d+\-\d+\-\d+)/',"weekly",name="weekly"),
  #url(r'weekly/(\d+\-\d+\-\d+)/(?P<page_number>\d+)/',"weekly",name="weekly"),
  #url(r'^(?P<page_number>\d+)/$', 'index', name="event_list"),
  #url(r'^tagged/(?P<slug>[^/]+)/(?P<page_number>\d+)/$', 'index', name="tagged"),
  url(r'^detail/(\d+)/(.+)/$', 'detail', name="event_detail"),
  url(r'^rsvp/$', 'rsvp', name='rsvp'),
  url(r'^checkin/$', 'checkin', name='rsvp'),
  url(r'^orientations/$','orientations',name='orientations'),
  url(r'^orientations/(\d+)/(\d+)/(\d+)/$','orientations',name='orientations'),
)
