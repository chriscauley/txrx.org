from django.urls import path

from . import views

urlpatterns = [
  path('rfid_access.json',views.door_access,name='door_access_json'),
  path('rfid_permission_table/',views.permission_table),
  path('api/rfid_log/',views.rfid_log,name='rfid_log'),
]
