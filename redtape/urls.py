from django.conf.urls import url, patterns

urlpatterns = patterns(
  'redtape.views',
  url(r'^(\d+)/(.*)$','document_detail',name='signed_document'),
  url(r'^save/(\d+)/$','document_json',name='document_json'),
  url(r'^required/$','index',name='redtape_index'),
  url(r'^documents.json$','documents_json'),
  url(r'^aggregate/(\d+)/$','aggregate',name='redtape')
)
