from django.conf.urls import url, patterns

urlpatterns = patterns(
  'instagram.views',
  url(r'^$','index',name="index"),
)
