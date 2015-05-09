from django.conf.urls import patterns, url, include
from django.contrib.sitemaps import views as sitemaps_views
from django.http import HttpResponse

urlpatterns = patterns(
  'blog.views',

  url(r'^admin/add/$', 'edit', name="add"),
  url(r'^admin/edit/(?P<pk>\d+)/$', 'edit', name="edit"),
  url(r'^admin/delete/(?P<pk>\d+)/$', 'delete', name="delete"),
  url(r'^admin/drafts/$', 'drafts', name="drafts"),
  url(r'^admin/preview/$', 'render_preview', name="render_preview"),
)

username_regex = '(?P<username>[\w\d\-\.\@\_]+)'
urlpatterns += patterns(
  'blog.views',
  url(r'^tag/(.+)/$','posts_by_tag',name='posts_by_tag'),
  url(r'^%s/(?P<slug>[\w\d\-]+)/$'%username_regex, 'post_detail', name="post_detail"),
  url(r'^%s/$'%username_regex, 'post_list', name="post_list"),
)

urlpatterns += patterns(
  '',
  (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nCrawl-delay: 5", content_type="text/plain")),
)
