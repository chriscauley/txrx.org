from django.conf.urls import url, patterns

import views, lablackey.views

urlpatterns = [
  url(r'^(\d+)/(.*)/$', lablackey.views.single_page_app,name='signed_document'),
  url(r'^save/(\d+)/$', views.document_json,name='document_json'),
  url(r'^required/$', views.index,name='redtape_index'),
  url(r'^documents.json$', views.documents_json),
  url(r'^document/add/(\d+)/$', views.post_document),
  url(r'^aggregate/(\d+)/$', views.aggregate,name='redtape'),
]
