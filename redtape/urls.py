from django.conf.urls import url, patterns

import views

urlpatterns = [
  url(r'^(\d+)/(.*)$', views.document_detail,name='signed_document'),
  url(r'^save/(\d+)/$', views.document_json,name='document_json'),
  url(r'^required/$', views.index,name='redtape_index'),
  url(r'^documents.json$', views.documents_json),
  url(r'^aggregate/(\d+)/$', views.aggregate,name='redtape')
]
