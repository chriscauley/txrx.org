from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import os

from context_processors import _nav

admin.autodiscover()

j = "(?:.json)?"

ms = "article|project"
urlpatterns = patterns(
    'views',
    (r'^$','home'),
    (r'^home%s$'%j,'home'),
    (r'^news/',include('articles.urls')),
    (r'^(?P<model>%s)/$'%ms,'feed'),
    (r'^(?P<model>%s)/(?P<year>\d{4})/(?P<slug>[\w\-\d]*)/$'%ms,'item'),
    (r'^admin/', include(admin.site.urls)),
    (r'^members/$','members'),
    (r'^member/(?P<username>.*)/$','member'),
    (r'^instructors/$','instructors'),
    (r'^classes%s'%j, 'classes'),
    (r'^projects/(?P<slug>[\w\d\-]*)/?$','projects'),
    (r'^survey/$','survey'),
    (r'^login','login'),
    (r'^logout','logout'),
    (r'^tools/?(?P<lab>[\w\d\-]*)/?(?P<tool>[\w\d\-]*)/','tools'),
    (r'^(?P<name>about)%s'%j,'generic'),
    (r'^(?P<name>join-us)%s'%j,'generic'),
    (r'^google_login','google_login'),
    (r'^google_return/(?P<url>.*)','google_return'),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^.*.json','comming_soon'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        #url(r'^static/(?P<path>.*)$',
        #    'django.views.static.serve',
        #    {'document_root': os.path.join(settings.SPATH, 'static'),
        #     'show_indexes': True}),
        url(r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': os.path.join(settings.SPATH, 'media'),
             'show_indexes': True}),
        )

