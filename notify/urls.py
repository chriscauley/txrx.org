from django.conf.urls import url

import views

urlpatterns = [
  url(r'^follow/([^/]+)/(\d+)/',views.follow,name='notify_follow'),
  url(r'^unfollow/(\d+)/',views.unfollow,name='notify_unfollow'),
  url(r'^notify_course/(\d+)/$',views.notify_course,name='notify_course'),
  url(r'^clear_notification/(notify_course)/(\d+)/(\d+)/$',views.clear_notification,
      name='clear_notification'),
  url(r'^unsubscribe/(notify_course|global|comments|classes|sessions)/(\d+)/$',
      views.unsubscribe, name='unsubscribe'),
]
