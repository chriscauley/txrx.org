from django.conf.urls import url

import views

urlpatterns = [
  url(r'^follow/([^/]+)/(\d+)/',views.follow,name='notify_follow'),
  url(r'^unfollow/(\d+)/',views.unfollow,name='notify_unfollow'),
  url(r'^unsubscribe/(notify_course|global|comments|classes|sessions)/(\d+)/$',
      views.unsubscribe, name='unsubscribe'),
]
