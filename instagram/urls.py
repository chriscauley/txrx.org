from django.conf.urls.defaults import *
urlpatterns = patterns(
  'instagram.views',
  url(r'^$','index',name="index"),
)
