from django.urls import path, re_path

from . import views

urlpatterns = [
  re_path(r'^follow/([^/]+)/(\d+)/',views.follow,name='notify_follow'),
  re_path(r'^unfollow/(\d+)/',views.unfollow,name='notify_unfollow'),
  re_path(r'^unsubscribe/(notify_course|global|comments|classes|sessions)/(\d+)/$',
      views.unsubscribe, name='unsubscribe'),
  path('settings/',views.settings,name='notify_settings'),
]
