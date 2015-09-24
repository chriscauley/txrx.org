from django.conf.urls import url, patterns

urlpatterns = patterns(
  'api.views',
  url('^([\w\d_]+)/([\w\d_]+)/$','list_view',name="api_list_view"),
  url('^([\w\d_]+)/([\w\d_]+)/(\d+)/$','detail_view',name="api_detail_view"),
)
