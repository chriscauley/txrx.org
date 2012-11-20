from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import os

admin.autodiscover()

_urls = lambda *ns: [url(r'^%s/'%n, include('%s.urls'%n, namespace=n, app_name=n)) for n in ns]
j = "(?:.json)?"

urlpatterns = patterns(
  'txrx.views',
  (r'^admin/', include(admin.site.urls)),
  (r'^members/$','members'),
  (r'^member/(?P<username>.*)/$','member'),
  (r'^membership/$', include('membership.urls')),
  (r'^$','course.views.index'),
  (r'^classes/', include('course.urls',namespace='course',app_name='course')),
  (r'^weblog/', include('zinnia.urls')),
  (r'^comments/', include('django.contrib.comments.urls')),
  (r'^projects/(?P<slug>[\w\d\-]*)/?$','projects'),
  (r'^survey/$','survey'),
  (r'^tools/?(?P<lab>[\w\d\-]*)/?(?P<tool>[\w\d\-]*)/','tools'),
  (r'^google_login','google_login'),
  (r'^google_return/(?P<url>.*)','google_return'),
  (r'^grappelli/', include('grappelli.urls')),
  (r'^accounts/', include('registration.backends.default.urls')),
  (r'^tx/rx/ipn/handler/', include('paypal.standard.ipn.urls')),
  (r'^password-reset/', include('password_reset.urls')),
  (r'^force_login/(\d+)/$', 'force_login'),
  #(r'^comments/', include('mptt_comments.urls')),
)

urlpatterns += patterns(
  '',
  url(r'^instructors/$','course.views.instructors',name='instructor_detail'),
  url(r'^instructors/([^/]+)/$','course.views.instructor_detail',name='instructor_detail'),
  #(r'^$','course.views.index'),
  (r'^join-us/$','membership.views.join_us'),
  (r'^new-classes$','course.views.index'),
  (r'^new_classes$','course.views.index'),
  (r'^main','course.views.index'),
  (r'^latest$','course.views.index'),
  (r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset',
   {'post_reset_redirect' : '/accounts/password/reset/done/'}),
  (r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
  (r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
   'django.contrib.auth.views.password_reset_confirm',
   {'post_reset_redirect' : '/accounts/password/done/'}),
  (r'^accounts/password/done/$', 'django.contrib.auth.views.password_reset_complete'),
  (r'^',include('django.contrib.flatpages.urls')),
)
# hardcoded urls for content pages. Will be created when a super user hits the address.
#urlpatterns += patterns(
#  '',
#  url(r'^(about-us)','lablackey.content.views.page',name='about_us'),
#)
if settings.DEBUG:
  urlpatterns += patterns(
    '',
    url(r'^media/(?P<path>.*)$',
      'django.views.static.serve',
      {'document_root': settings.MEDIA_ROOT,
       'show_indexes': True}),
    )

