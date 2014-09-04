from django.conf.urls.defaults import *

urlpatterns = patterns(
  'event.views',
  url(r'^$', 'index', name="index"),
  url(r'^(\d+\-\d+\-\d+)/$', 'index', name="index"),
  url(r'^occurrence/(\d+)/$','occurrence_detail',name='occurrence_detail'),
  url(r'^(\d+)/(.+)/$','occurrence_detail',name='occurrence_detail'),
  url(r'ics/([^/]+)/([^/]+)/(\d+)/(.+).ics','ics',name="ics"),
  url(r'ics/(all_events).ics','all_ics',name="all_ics"),
  #url(r'weekly/(\d+\-\d+\-\d+)/',"weekly",name="weekly"),
  #url(r'weekly/(\d+\-\d+\-\d+)/(?P<page_number>\d+)/',"weekly",name="weekly"),
  #url(r'^(?P<page_number>\d+)/$', 'index', name="event_list"),
  #url(r'^tagged/(?P<slug>[^/]+)/(?P<page_number>\d+)/$', 'index', name="tagged"),
  #url(r'^detail/(\d+)/$', 'detail', name="detail"),

  # Depracated
  #url(r'^repeat/(monthly|weekly)/(\d+)/$','repeat_event',name='repeat_event'),
)
