from django.conf.urls import url

import views

urlpatterns = [
  url(r'^join-us/$',views.join_us,name="join_us"),
  url(r'^minutes/$', views.minutes_index, name='meeting_minutes_index',),
  url(r'^minutes/(\d+-\d+-\d+)/$', views.minutes, name='meeting_minutes',),
  url(r'^roland_email/$',views.roland_email,name='roland_email'),
  url(r'^roland_email/(\d+)/(\d+)/(\d+)/$',views.roland_email,name='roland_email'),
  url(r'^api/users/$',views.user_emails),
  url(r'^api/courses/$',views.course_names),
  url(r'^instructors/$',views.member_index,name='instructor_index'),
  url(r'^instructors/([^/]+)/$',views.member_detail,name='instructor_detail'),
  url(r'^u/$',views.member_index,name='member_index'),
  url(r'^u/([^/]+)/$',views.member_detail,name='member_detail'),
  url(r'^officers/$', views.officers, name='officers'),
  url(r'^analysis/$', views.analysis, name='analysis'),
  url(r'^force_cancel/(\d+)/$',views.force_cancel,name="force_cancel"),
  url(r'^flag_subscription/(\d+)/$',views.flag_subscription,name="flag_subscription"),
  url(r'^update_flag_status/(\d+)/$',views.update_flag_status,name='update_flag_status'),
  url(r'^update_flag_status/(\d+)/([\w\d\-\_]+)/$',views.update_flag_status,name='update_flag_status'),
  url(r'^containers/$',views.containers),
  url(r'^membership/container/(\d+)/',views.container,name='container'),
]
