from django.conf.urls import *

import views

urlpatterns = [
  url(r'^$', views.index, name="index"),
  url(r'^(\d+\-\d+\-\d+)/$', views.index, name="index"),
  url(r'^occurrence/(\d+)/$', views.occurrence_detail,name='occurrence_detail'),
  url(r'^(\d+)/(.+)/$', views.occurrence_detail,name='occurrence_detail'),
  url(r'ics/([^/]+)/([^/]+)/(\d+)/(.+).ics', views.ics,name="ics"),
  url(r'ics/(all_events).ics', views.all_ics,name="all_ics"),
  url(r'eventdetail_(\d+).json', views.detail_json),
  #url(r'weekly/(\d+\-\d+\-\d+)/', views.weekly,name="weekly"),
  #url(r'weekly/(\d+\-\d+\-\d+)/(?P<page_number>\d+)/',views.weekly,name="weekly"),
  #url(r'^(?P<page_number>\d+)/$', views.index, name="event_list"),
  #url(r'^tagged/(?P<slug>[^/]+)/(?P<page_number>\d+)/$', views.index, name="tagged"),
  url(r'^detail/(\d+)/(.+)/$', views.detail, name="event_detail"),
  url(r'^rsvp/$', views.rsvp, name='rsvp'),
  url(r'^checkin/$', views.checkin, name='rsvp'),
  url(r'^no-orientation/$',views.no_orientation,name='no_orientation'),
  url(r'^orientations/$', views.orientations,name='orientations'),
  url(r'^orientations/(\d+)/(\d+)/(\d+)/$', views.orientations,name='orientations'),
  url(r'^(own|disown)/(\d+)/',views.owner_ajax),
  url(r'^bulk.json$',views.bulk_ajax),
]
