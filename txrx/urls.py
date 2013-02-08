from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import os

admin.autodiscover()

_urls = lambda *ns: [url(r'^%s/'%n, include('%s.urls'%n, namespace=n, app_name=n)) for n in ns]

urlpatterns = patterns(
  '',
  url(r'^$','txrx.views.blog_home',name="home"),
  (r'^admin/', include(admin.site.urls)),
  (r'^membership/$', include('membership.urls')),
  (r'^classes/', include('course.urls',namespace='course',app_name='course')),
  (r'^blog/$','txrx.views.blog_home'),
  (r'^blog/',include('codrspace.urls')),
  (r'^survey/$','txrx.views.survey'),
  (r'^grappelli/', include('grappelli.urls')),
  url(r'^accounts/settings/$','membership.views.settings',name='account_settings'),
  (r'^accounts/', include('registration.backends.default.urls')),
  (r'^tx/rx/ipn/handler/', include('paypal.standard.ipn.urls')),
  (r'^password-reset/', include('password_reset.urls')),
  (r'^force_login/(\d+)/$', 'txrx.views.force_login'),
  (r'^tools/',include('tool.urls')),
  (r'^500/$','txrx.views.intentional_500'),
  url(r'^event/',include('event.urls',namespace="event",app_name="event")),
  url(r'^instagram/',include('instagram.urls',namespace="instagram",app_name="instagram")),

  # comments and javascript translation
  (r'^comments/', include('mptt_comments.urls')),
  url(r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
)

urlpatterns += patterns(
  '',
  url(r'^instructors/$','course.views.instructors',name='instructor_detail'),
  url(r'^instructors/([^/]+)/$','course.views.instructor_detail',name='instructor_detail'),
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
)

# flat pages
urlpatterns += patterns(
  '',
  url(r'^(map/)$','django.contrib.flatpages.views.flatpage',name='map'),
)

if settings.DEBUG:
  urlpatterns += patterns(
    '',
    url(r'^media/(?P<path>.*)$',
      'django.views.static.serve',
      {'document_root': settings.MEDIA_ROOT,
       'show_indexes': True}),
    )

