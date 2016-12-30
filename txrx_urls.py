from django.conf.urls import url

import lablackey.views

urlpatterns = [
  url(r'^work/$',lablackey.views.single_page_app),
]
