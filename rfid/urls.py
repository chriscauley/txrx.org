from django.conf.urls import url

import views

urlpatterns = [
  url(r'^rfid_access.json$',views.door_access,name='door_access_json'),
  url(r'^rfid_permission_table/$',views.permission_table),
  url(r'^api/rfid_log/$',views.rfid_log,name='rfid_log'),
]
