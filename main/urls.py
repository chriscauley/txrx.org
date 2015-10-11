from django.conf import settings
from django.conf.urls import url, patterns, include
from django.contrib import admin
from django.contrib.auth.views import password_reset
from django.contrib.flatpages.models import FlatPage
from django.contrib.sitemaps.views import sitemap

from main.sitemaps import sitemaps
from main.feeds import AllFeed

import os

_urls = lambda *ns: [url(r'^%s/'%n, include('%s.urls'%n, namespace=n, app_name=n)) for n in ns]

urlpatterns = patterns(
  '',
  url(r'^$','main.views.index',name="home"),
  url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
  url(r'^admin/', include(admin.site.urls)),
  url(r'^blog/',include('blog.urls')),
  url(r'^(\d{4})/(\d{1,2})/(\d{1,2})/([^/]+)/','blog.views.post_redirect'),
  url(r'^500/$','main.views.intentional_500'),
  url(r'^event/',include('event.urls',namespace="event",app_name="event")),
  url(r'^instagram/',include('instagram.urls',namespace="instagram",app_name="instagram")),
  url(r'^media_files/',include('media.urls')),
  url(r'^shop/',include('store.urls')),
  url(r'^products.js$','store.views.products_json'),

  # comments and javascript translation
  url(r'^comments/',include('mptt_comments.urls')),
  url(r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
  url(r'^rss/$', AllFeed()),
  url(r'^favicon.ico$','main.views.predirect',
      kwargs={'url':getattr(settings,'FAVICON','/static/favicon.ico')}),
  url(r'^thing/$','thing.views.thing_index',name='thing_index'),
  url(r'^thing/add/$','thing.views.add_thing',name='add_thing'),
  url(r'^thing/(\d+)/([\w\d\-\_]+)/$','thing.views.thing_detail',name='thing_detail'),
  url(r'^gfycat/$','main.views.gfycat',name='gfycat'),
  url(r'^tools/',include('tool.urls')),
  url('', include('social.apps.django_app.urls', namespace='social')),
  url(r'perfect-programming','main.views.intentional_500'),
  url(r'^classes/', include('course.urls',namespace='course',app_name='course')),
  url(r'^tx/rx/ipn/handler/', include('paypal.standard.ipn.urls')),
  url(r'^tx/rx/return/$','course.views.paypal_return',name='paypal_redirect'),
  url(r'^contact/$','contact.views.contact',name='contact'),
  url(r'^dxfviewer/$','geo.views.dxfviewer',name='dxfviewer'),
  url(r'^checkin/$', 'user.views.checkin', name='checkin'),
  url(r'^user.json','user.views.user_json'),
)

def activate_user(target):
  def wrapper(request,*args,**kwargs):
    from django.contrib.auth import get_user_model
    model = get_user_model()
    if request.REQUEST.get('email',None):
      try:
        user = model.objects.get(email=request.REQUEST.get('email'))
        user.is_active = True
        user.save()
      except model.DoesNotExist:
        pass
    return target(request,*args,**kwargs)
  return wrapper

#auth related
urlpatterns += patterns(
  '',
  url(r'^accounts/settings/$','membership.views.user_settings',name='account_settings'),
  url(r'^accounts/register/$','membership.views.register'),
  url(r'^accounts/', include('registration.urls')),
  url(r'^auth/password_reset/$',activate_user(password_reset)),
  url(r'^auth/',include('django.contrib.auth.urls')),
  url(r'^force_login/(\d+)/$', 'main.views.force_login'),
  url(r'^api/',include("api.urls")),
  url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
)

#membership urls
urlpatterns += patterns(
  'membership.views',
  url(r'^join-us/$','join_us'),
  url(r'^minutes/$', 'minutes_index', name='meeting_minutes_index',),
  url(r'^minutes/(\d+-\d+-\d+)/$', 'minutes', name='meeting_minutes',),
  url(r'^roland_email/$','roland_email',name='roland_email'),
  url(r'^roland_email/(\d+)/(\d+)/(\d+)/$','roland_email',name='roland_email'),
  url(r'^api/users/$','user_emails'),
  url(r'^api/courses/$','course_names'),
  url(r'^api/completions/$','course_completion'),
  url(r'^instructors/$','member_index',name='instructor_index'),
  url(r'^instructors/([^/]+)/$','member_detail',name='instructor_detail'),
  url(r'^u/$','member_index',name='member_index'),
  url(r'^u/([^/]+)/$','member_detail',name='member_detail'),
  url(r'^officers/$', 'officers', name='officers'),
  url(r'^analysis/$', 'analysis', name='analysis'),
  url(r'^force_cancel/(\d+)/$','force_cancel',name="force_cancel"),
  url(r'^flag_subscription/(\d+)/$','flag_subscription',name="flag_subscription"),
  url(r'^containers/$','containers'),
  url(r'^update_flag_status/(\d+)/$','update_flag_status',name='update_flag_status'),
  url(r'^update_flag_status/(\d+)/([\w\d\-\_]+)/$','update_flag_status',name='update_flag_status'),
)

#notify urls
urlpatterns += patterns(
  'notify.views',
  url(r'^notify_course/(\d+)/$','notify_course',name='notify_course'),
  url(r'^clear_notification/(notify_course)/(\d+)/(\d+)/$','clear_notification',name='clear_notification'),
  url(r'^unsubscribe/(notify_course|global|comments|classes|sessions)/(\d+)/$',
      'unsubscribe', name='unsubscribe'),
)

# todo
urlpatterns += patterns(
  '',
  (r'^survey/$','main.views.survey'),
)

flatpages = [page.url[1:] for page in FlatPage.objects.all()]
fps = '|'.join(flatpages)

# flat pages
urlpatterns += patterns(
  '',
  url(r'^(about-us)/$','main.views.to_template'),
  url(r'(%s)'%fps,'django.contrib.flatpages.views.flatpage',name='map'),
)

if settings.DEBUG:
  urlpatterns += patterns(
    '',
    url(r'^media/(?P<path>.*)$','django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT,'show_indexes': True}),
  )

