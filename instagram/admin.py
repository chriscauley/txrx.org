from .models import InstagramPhoto, InstagramLocation
from django.contrib import admin

class InstagramPhotoAdmin(admin.ModelAdmin):
  list_display = ("thumbnail_","approved",'rejected',"username","caption")
  list_editable = ("approved",'rejected')
  list_filter = ("approved",'rejected')

admin.site.register(InstagramPhoto,InstagramPhotoAdmin)
admin.site.register(InstagramLocation)
