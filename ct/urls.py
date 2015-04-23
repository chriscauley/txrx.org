from django.conf.urls.defaults import url, patterns

urlpatterns = patterns(
  'ct.views',
  url('^$','index'),
)
