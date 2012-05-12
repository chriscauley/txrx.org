from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin
import os
admin.autodiscover()

_urls = lambda *ns: [url(r'^%s/'%n, include('%s.urls'%n, namespace=n, app_name=n)) for n in ns]

urlpatterns = patterns(
  '',
  url(r'^$', "views.home", name="home"),
  url(r'^admin/update_occurrences/(\d+)/',"chores.views.update_occurrences"),
  url(r'^admin/', include(admin.site.urls)),
  (r'^grappelli/', include('grappelli.urls')),
  (r'^ajax_select/', include('ajax_select.urls')),
  *_urls('chores')
)

favicon = '%sfavicon.ico'%settings.STATIC_URL
if settings.DEBUG:
  favicon = '%smwm.ico'%settings.STATIC_URL
  urlpatterns += patterns(
    '',
    url(r'^site_media/static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': os.path.join(settings.SPATH, 'static'),
         'show_indexes': True}),
    url(r'^site_media/media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': os.path.join(settings.SPATH, 'media'),
         'show_indexes': True}),
    )

urlpatterns += patterns(
  'django.views.generic.simple',
  (r'^favicon.ico$', 'redirect_to',{'url': favicon}),
)
