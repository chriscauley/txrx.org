from django.conf import settings
from django.conf.urls import url, patterns, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset
from django.contrib.flatpages.models import FlatPage
from django.contrib.sitemaps.views import sitemap

from main.sitemaps import sitemaps
from main.feeds import AllFeed
from main import views as main_views

import blog.urls, blog.views
import store.urls, media.urls, event.urls, thing.views, tool.urls, tool.views
import paypal.standard.ipn.urls
import social.apps.django_app.urls
import unrest_comments.urls
import course.urls, course.views
import djstripe.urls
import contact.views
import geo.views
import user.views
import redtape.urls
import membership.urls
import registration.urls

import os

_urls = lambda *ns: [url(r'^%s/'%n, include('%s.urls'%n, namespace=n, app_name=n)) for n in ns]

_pages = [
  'checkin',
  'checkout',
  'todays-checkins',
  'my-permissions',
  'needed-sessions',
  'rooms',
  'rfid',
  'toolmaster',
  'week-hours',
]

urlpatterns = [
  url(r'^(%s)/$'%('|'.join(_pages)),main_views.beta),
  url(r'^$',main_views.index,name="home"),
  url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
  url(r'^admin/', include(admin.site.urls)),
  url(r'^blog/',include(blog.urls)),
  url(r'arst/(?P<pk>\d+)',main_views.intentional_500,name="order_detail"),
  url(r'^(\d{4})/(\d{1,2})/(\d{1,2})/([^/]+)/',blog.views.post_redirect),
  url(r'^500/$',main_views.intentional_500),
  url(r'^event/',include(event.urls,namespace="event",app_name="event")),
  url(r'^media_files/',include(media.urls)),
  url(r'^shop/',include(store.urls)),
  url(r'^product_is_a_fail/(.*)/$',main_views.index,name="product_detail"),
  url(r'^me/$',login_required(main_views.beta)),
  url(r'^comments/',include(unrest_comments.urls)),
  url(r'^rss/$', AllFeed()),
  url(r'^favicon.ico$',main_views.predirect,
      kwargs={'url':getattr(settings,'FAVICON','/static/favicon.ico')}),
  url(r'^sculpturemonth$',main_views.predirect,
      kwargs={'url':"/classes/221/3d-modeling-with-rhino/?rhino10"}),
  url(r'^thing/$',thing.views.thing_index,name='thing_index'),
  url(r'^thing/add/$',thing.views.add_thing,name='add_thing'),
  url(r'^thing/(\d+)/([\w\d\-\_]+)/$',thing.views.thing_detail,name='thing_detail'),
  url(r'^gfycat/$',main_views.gfycat,name='gfycat'),
  url(r'^tools/',include(tool.urls)),
  url(r'^borrow/$',tool.views.checkout_items,name='checkout_items'),
  url('', include(social.apps.django_app.urls, namespace='social')),
  url(r'perfect-programming',main_views.intentional_500),
  url(r'^classes/', include(course.urls,namespace='course',app_name='course')),
  url(r'^tx/rx/ipn/handler/', include(paypal.standard.ipn.urls)),
  url(r'^tx/rx/return/$',course.views.paypal_return,name='paypal_redirect'),
  url(r'^payments/', include(djstripe.urls, namespace="djstripe")),
  url(r'^contact/$',contact.views.contact,name='contact'),
  url(r'^contact/(\w+).(\w+)_(\d+)-(.*).png$',contact.views.tracking_pixel,name="tracking_pixel"),
  url(r'^dxfviewer/$',geo.views.dxfviewer,name='dxfviewer'),
  url(r'^geo/events.json',geo.views.events_json),
  url(r'^geo/locations.json$',geo.views.locations_json),
  url(r'^checkin_ajax/$', user.views.checkin_ajax, name='checkin_ajax'),
  url(r'^add_rfid/$', user.views.add_rfid, name='add_rfid'),
  url(r'^user.json',user.views.user_json),
  url(r'^todays_checkins.json',user.views.todays_checkins_json),
  url(r'^redtape/',include(redtape.urls)),
]

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

def _include(s):
  return include(__import__(s).urls)

import membership.views
import django.contrib.auth.urls

#auth related
urlpatterns += [
  url(r'^accounts/settings/$',membership.views.user_settings,name='account_settings'),
  url(r'^accounts/register/$',membership.views.register),
  url(r'^accounts/(cancel)_subscription/',membership.views.change_subscription,name="cancel_subscription"),
  url(r'^accounts/', include(registration.urls)),
  url(r'^auth/password_reset/$',activate_user(password_reset)),
  url(r'^auth/',include(django.contrib.auth.urls)),
  url(r'^force_login/(\d+)/$', main_views.force_login),
  url(r'^api/remove_rfid/$',user.views.remove_rfid),
  url(r'^api/change_rfid/$',user.views.set_rfid),
  url(r'^api/user_checkin/$',user.views.user_checkin),
  url(r'^api/',_include('api.urls')),
  url(r'^api/change_(headshot|id_photo)/$',user.views.change_headshot),
  #url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
]

urlpatterns += [
  url(r'',_include('membership.urls')),
  url(r'',_include('rfid.urls')),
  url(r'',_include('notify.urls')),
  url(r'^survey/$',main_views.survey), #! TODO
]

if hasattr(settings,"STAFF_URL"):
  urlpatterns += [url(settings.STAFF_URL[1:],user.views.hidden_image)]

flatpages = [page.url[1:] for page in FlatPage.objects.all()]
fps = '|'.join(flatpages)

import django.contrib.flatpages.views
# flat pages
urlpatterns += [
  url(r'^(about-us)/$',main_views.to_template),
  url(r'(%s)'%fps,django.contrib.flatpages.views.flatpage,name='map'),
]

from django.views.static import serve
from django.contrib.auth.decorators import user_passes_test

is_superuser = lambda user:user.is_superuser
urlpatterns += [
    url(r'^media/(?P<path>signatures/.*)$',user_passes_test(is_superuser)(serve),
        {'document_root': settings.MEDIA_ROOT,'show_indexes': False})
]
if settings.DEBUG:
  urlpatterns += [
    url(r'^media/(?P<path>.*)$',serve,
        {'document_root': settings.MEDIA_ROOT,'show_indexes': True})
  ]

# Turn me on to enable "maintenance mode"
if False:
  urlpatterns = [
    url(r'^(maintenance)/$',main_views.beta),
    url(r'^admin/', include(admin.site.urls)),
    url(r'',main_views.predirect,kwargs={'url': "/maintenance/"},name="logout"),
  ]
