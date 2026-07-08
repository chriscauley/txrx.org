from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.flatpages.models import FlatPage
from django.contrib.sitemaps.views import sitemap
from django.db.utils import ProgrammingError

from main.sitemaps import sitemaps
from main.feeds import AllFeed
import main.views, main.dashboard

import lablackey.blog.views
import store.urls, media.urls, event.urls, thing.views, tool.urls, tool.views
import paypal.standard.ipn.urls
import social_django.urls
import unrest_comments.urls
import course.urls, course.views
import djstripe.urls
import contact.views, lablackey.geo.views, user.views
import redtape.urls
import membership.urls
import course.views.classes
import txrx.urls
from lablackey.sms import urls as sms_urls
from lablackey.decorators import activate_user

import os

_pages = [
  'checkin',
  'checkout',
  'todays-checkins',
  'my-permissions',
  'needed-sessions',
  'rooms',
  'toolmaster',
  'week-hours',
  'me',
  'admin/dashboard',
  'notify',
  'event/bulk',
  'auth/login'
]

urlpatterns = [
  re_path(r'^(%s)/$'%('|'.join(_pages)),main.views.beta),
  path('',main.views.index,name="home"),
  path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
  re_path(r'^dashboard/totals.(json|csv|table)$', main.dashboard.totals_json),
  path('admin/', admin.site.urls),
  re_path(r'arst/(?P<pk>\d+)',main.views.intentional_500,name="order_detail"),
  re_path(r'^(\d{4})/(\d{1,2})/(\d{1,2})/([^/]+)/',lablackey.blog.views.post_redirect),
  path('500/',main.views.intentional_500),
  path('event/',include((event.urls,"event"),namespace="event")),
  path('media_files/',include(media.urls)),
  path('shop/',include(store.urls)),
  re_path(r'^product_is_a_fail/(.*)/$',main.views.index,name="product_detail"),
  path('comments/',include(unrest_comments.urls)),
  path('rss/', AllFeed()),
  path('favicon.ico',main.views.predirect,
      kwargs={'url':getattr(settings,'FAVICON','/static/favicon.ico')}),
  path('sculpturemonth',main.views.predirect,
      kwargs={'url':"/classes/221/3d-modeling-with-rhino/?rhino10"}),
  path('rapidfabstudio',main.views.predirect,
      kwargs={'url':"/event/detail/133/rapid-fab-studio-hours/"}),
  path('3dprinting/',main.views.predirect,
      kwargs={'url':"/classes/37/3d-printing-i/"}),
  path('thing/',thing.views.thing_index,name='thing_index'),
  path('thing/add/',thing.views.add_thing,name='add_thing'),
  re_path(r'^thing/(\d+)/([\w\d\-\_]+)/$',thing.views.thing_detail,name='thing_detail'),
  path('gfycat/',main.views.gfycat,name='gfycat'),
  path('tools/',include(tool.urls)),
  path('borrow/',tool.views.checkout_items,name='checkout_items'),
  path('', include((social_django.urls,'social'), namespace='social')),
  re_path(r'perfect-programming',main.views.intentional_500),
  path('classes/', include((course.urls,'course'),namespace='course')),
  path('gift/',course.views.classes.index),
  path('tx/rx/ipn/handler/', include(paypal.standard.ipn.urls)),
  path('tx/rx/return/',course.views.paypal_return,name='paypal_redirect'),
  path('payments/', include((djstripe.urls,"djstripe"), namespace="djstripe")),
  path('contact/',contact.views.contact,name='contact'),
  re_path(r'^contact/(\w+).(\w+)_(\d+)-(.*).png$',contact.views.tracking_pixel,name="tracking_pixel"),
  path('dxfviewer/',lablackey.geo.views.dxfviewer,name='dxfviewer'),
  re_path(r'^geo/events.json',lablackey.geo.views.events_json),
  path('geo/locations.json',lablackey.geo.views.locations_json),
  path('checkin_ajax/', user.views.checkin_ajax, name='checkin_ajax'),
  path('checkin_email/', user.views.checkin_email, name='checkin_email'),
  path('checkin_register/', user.views.checkin_register, name='checkin_register'),
  path('add_rfid/', user.views.add_rfid, name='add_rfid'),
  re_path(r'^user.json',user.views.user_json),
  re_path(r'^todays_checkins.json',user.views.todays_checkins_json),
  path('redtape/',include(redtape.urls)),
  path('',include(txrx.urls)),
  path('',include(sms_urls)),
]

def _include(s):
  return include(__import__(s).urls)

import membership.views
import django.contrib.auth.urls
import lablackey.urls
import notify.urls
from user.forms import PasswordResetForm

#auth related
urlpatterns += [
  path('accounts/settings/',membership.views.user_settings,name='account_settings'),
  path('accounts/register/',membership.views.register,name="account_register"),
  re_path(r'^accounts/(cancel)_subscription/',membership.views.change_subscription,name="cancel_subscription"),
  #! TODO Move the following to lablackey.registration, write test, and make activate AFTER password is reset
  path('auth/password_reset/',activate_user(PasswordResetView.as_view(form_class=PasswordResetForm))),
  path('auth/',include(django.contrib.auth.urls)),
  re_path(r'^force_login/([\d\w]+)/$', main.views.force_login),
  path('api/remove_rfid/',user.views.remove_rfid),
  path('api/change_rfid/',user.views.set_rfid),
  path('api/user_checkin/',user.views.user_checkin),
  re_path(r'^api/change_(headshot|id_photo)/$',user.views.change_headshot),
  re_path(r'',_include('membership.urls')),
  re_path(r'',_include('rfid.urls')),
  path('',include(lablackey.urls)),
  path('notify/',include(notify.urls)),
]

if hasattr(settings,"STAFF_URL"):
  urlpatterns += [re_path(settings.STAFF_URL[1:],user.views.hidden_image)]

urlpatterns += [
  re_path(r'^(about-us)/$',main.views.to_template),
]

from django.views.static import serve
from django.contrib.auth.decorators import user_passes_test

is_superuser = lambda user:user.is_superuser
urlpatterns += [
    re_path(r'^media/(?P<path>signatures/.*)$',user_passes_test(is_superuser)(serve),
        {'document_root': settings.MEDIA_ROOT,'show_indexes': False})
]
if settings.DEBUG or True:
  urlpatterns += [
    re_path(r'^media/(?P<path>.*)$',serve,
        {'document_root': settings.MEDIA_ROOT,'show_indexes': True})
  ]

# Turn me on to enable "maintenance mode"
if False:
  urlpatterns = [
    re_path(r'^(maintenance)/$',main.views.beta),
    path('admin/', admin.site.urls),
    re_path(r'',main.views.predirect,kwargs={'url': "/maintenance/"},name="logout"),
  ]
