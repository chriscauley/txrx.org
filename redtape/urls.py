from django.urls import path, re_path

from . import views
import lablackey.views

urlpatterns = [
  re_path(r'^(\d+)/(.*)/$', lablackey.views.single_page_app,name='signed_document'),
  re_path(r'^save/(\d+)/$', views.document_json,name='document_json'),
  path('required/', views.index,name='redtape_index'),
  path('documents.json', views.documents_json),
  re_path(r'^document/add/(\d+)/$', views.post_document),
  re_path(r'^aggregate/(\d+)/$', views.aggregate,name='redtape'),
]
