from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns(
  'media.views',
  url(r'^photo/insert/$','insert_photo',name='insert_photo'),
  url(r'^photo/add/$','add_photo',name='add_photo'),
  url(r'^photo/bulk_tag/$','bulk_tag_index',name='bulk_tag_index'),
  url(r'^photo/bulk_tag/(\d+)/$','bulk_tag_detail',name='bulk_tag_detail'),
)
