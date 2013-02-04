from .models import InstagramPhoto, InstagramLocation
from django.contrib import admin

class InstagramPhotoAdmin(admin.ModelAdmin):
  list_display = ("thumbnail_","approved","username","caption")
  list_editable = ("approved",)
  list_filter = ("approved",)

admin.site.register(InstagramPhoto,InstagramPhotoAdmin)
admin.site.register(InstagramLocation)
