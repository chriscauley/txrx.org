from django.conf.urls.defaults import patterns, url, include
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps import views as sitemaps_views
from django.http import HttpResponse
from codrspace.feeds import LatestPostsFeed
from codrspace.api import PostResource
from codrspace.site_maps import DefaultMap, PostMap, UserMap

post_resource = PostResource()
site_maps = {
    'default': DefaultMap,
    'posts': PostMap,
    'users': UserMap
}

urlpatterns = patterns('codrspace.views',
    url(r'^$', 'index', name="homepage"),

    url(r'^admin/add/$', 'add', name="add"),
    url(r'^admin/edit/(?P<pk>\d+)/$', 'edit', name="edit"),
    url(r'^admin/delete/(?P<pk>\d+)/$', 'delete', name="delete"),
    url(r'^admin/drafts/$', 'drafts', name="drafts"),
    url(r'^admin/preview/$', 'render_preview', name="render_preview"),

    url(r'^settings/$', 'user_settings', name="user_settings"),
    url(r'^api-settings/', 'api_settings', name="api_settings"),

    url(r'^signin/$', 'signin_start', name="signin_start"),
    url(r'^signin_callback/$', 'signin_callback', name="signin_callback"),
    url(r'^signout/$', 'signout', name="signout"),

    url(r'^feedback/$', 'feedback', name="feedback"),
    url(r'^api/', include(post_resource.urls)),
)

urlpatterns += patterns('codrspace.mock_views',
    url(r'^fake_user/$', 'fake_user', name="fake_user"),
    url(r'^authorize/$', 'authorize', name="authorize"),
    url(r'^access_token/$', 'access_token', name="access_token"),
)
username_regex = '(?P<username>[\w\d\-\.\@\_]+)'
urlpatterns += patterns('codrspace.views',
    url(r'^%s/feed/$'%username_regex, LatestPostsFeed(), name="posts_feed"),
    url(r'^%s/(?P<slug>[\w\d\-]+)/$'%username_regex, 'post_detail', name="post_detail"),
    url(r'^%s/$'%username_regex, 'post_list', name="post_list"),
)

urlpatterns += patterns('',
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nCrawl-delay: 5", mimetype="text/plain")),
    (r'^sitemap\.xml$', cache_page(86400)(sitemaps_views.sitemap), {'sitemaps': site_maps})
)
