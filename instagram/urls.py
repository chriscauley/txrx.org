from django.urls import path

urlpatterns = patterns(
  'instagram.views',
  path('','index',name="index"),
)
