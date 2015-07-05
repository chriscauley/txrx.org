from django.conf.urls import patterns, url, include

urlpatterns = patterns(
  'media.views',
  url(r'^photo/search/$','photo_search',name='photo_search'),
  url(r'^photo/tag/$','tag_photo',name='tag_photo'),
  url(r'^photo/insert/$','insert_photo',name='insert_photo'),
  url(r'^photo/add/$','add_photo',name='add_photo'),
  url(r'^photo/bulk_tag/$','bulk_tag_index',name='bulk_tag_index'),
  url(r'^photo/bulk_tag/(\d+)/$','bulk_tag_detail',name='bulk_tag_detail'),
  url(r'^photo/bulk_upload/$','bulk_photo_upload',name='bulk_photo_upload'),
  url(r'^photo/untag/$','untag_photo',name='untag_photo'),
  url(r'^photo/delete/$','delete_photo',name='delete_photo'),
)
