from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    
    url(r'^redirect/$', login_redirect, name='membership.redirector',),
    
    )