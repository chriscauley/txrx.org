from django.urls import path, re_path

from . import views

urlpatterns = [
  path('join-us/',views.join_us,name="join_us"),
  path('minutes/', views.minutes_index, name='meeting_minutes_index',),
  re_path(r'^minutes/(\d+-\d+-\d+)/$', views.minutes, name='meeting_minutes',),
  path('roland_email/',views.roland_email,name='roland_email'),
  re_path(r'^roland_email/(\d+)/(\d+)/(\d+)/$',views.roland_email,name='roland_email'),
  path('api/users/',views.user_emails),
  path('api/courses/',views.course_names),
  path('instructors/',views.member_index,name='instructor_index'),
  re_path(r'^instructors/([^/]+)/$',views.member_detail,name='instructor_detail'),
  path('u/',views.member_index,name='member_index'),
  re_path(r'^u/([^/]+)/$',views.member_detail,name='member_detail'),
  path('officers/', views.officers, name='officers'),
  path('analysis/', views.analysis, name='analysis'),
  re_path(r'^force_cancel/(\d+)/$',views.force_cancel,name="force_cancel"),
  re_path(r'^flag_subscription/(\d+)/$',views.flag_subscription,name="flag_subscription"),
  re_path(r'^update_flag_status/(\d+)/$',views.update_flag_status,name='update_flag_status'),
  re_path(r'^update_flag_status/(\d+)/([\w\d\-\_]+)/$',views.update_flag_status,name='update_flag_status'),
  path('containers/',views.containers),
  re_path(r'^membership/container/(\d+)/',views.container,name='container'),
]
