from django.urls import re_path

from . import views

urlpatterns = [
  re_path(r'^$', views.index, name="index"),
  re_path(r'^(\d+\-\d+\-\d+)/$', views.index, name="index"),
  re_path(r'^occurrence/(\d+)/$', views.occurrence_detail,name='occurrence_detail'),
  re_path(r'^(\d+)/(.+)/$', views.occurrence_detail,name='occurrence_detail'),
  re_path(r'ics/([^/]+)/([^/]+)/(\d+)/(.+).ics', views.ics,name="ics"),
  re_path(r'ics/(all_events).ics', views.all_ics,name="all_ics"),
  re_path(r'eventdetail_(\d+).json', views.detail_json),
  #re_path(r'weekly/(\d+\-\d+\-\d+)/', views.weekly,name="weekly"),
  #re_path(r'weekly/(\d+\-\d+\-\d+)/(?P<page_number>\d+)/',views.weekly,name="weekly"),
  #re_path(r'^(?P<page_number>\d+)/$', views.index, name="event_list"),
  #re_path(r'^tagged/(?P<slug>[^/]+)/(?P<page_number>\d+)/$', views.index, name="tagged"),
  re_path(r'^detail/(\d+)/(.+)/$', views.detail, name="event_detail"),
  re_path(r'^rsvp/$', views.rsvp, name='rsvp'),
  re_path(r'^checkin/$', views.checkin, name='rsvp'),
  re_path(r'^no-orientation/$',views.no_orientation,name='no_orientation'),
  re_path(r'^orientations/$', views.orientations,name='orientations'),
  re_path(r'^orientations/(\d+)/(\d+)/(\d+)/$', views.orientations,name='orientations'),
  re_path(r'^bulk.json$',views.bulk_ajax),
]
