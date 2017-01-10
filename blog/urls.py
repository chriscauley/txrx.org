from django.conf.urls import patterns, url, include
from django.contrib.sitemaps import views as sitemaps_views
from django.http import HttpResponse

import views

username_regex = '(?P<username>[\w\d\-\.\@\_]+)'

urlpatterns = [
  url(r'^admin/add/$', views.edit, name="add"),
  url(r'^admin/edit/(?P<pk>\d+)/$', views.edit, name="edit"),
  url(r'^admin/delete/(?P<pk>\d+)/$', views.delete, name="delete"),
  url(r'^admin/drafts/$', views.drafts, name="drafts"),
  url(r'^admin/preview/$', views.render_preview, name="render_preview"),

  url(r'^tag/(.+)/$', views.posts_by_tag,name='posts_by_tag'),
  url(r'^(?P<username>\d+)/(?P<slug>[\w\d\-]+)/$', views.post_detail, name="post_detail"),
  url(r'^%s/(?P<slug>[\w\d\-]+)/$'%username_regex, views.post_detail, name="post_detail"),
  url(r'^%s/$'%username_regex, views.post_list, name="post_list"),
  url(r'^$', views.home,name="blog_home"),
]
