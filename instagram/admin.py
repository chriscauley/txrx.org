from .models import InstagramPhoto, InstagramLocation, InstagramTag, InstagramUser
from django.contrib import admin

class InstagramPhotoAdmin(admin.ModelAdmin):
  list_display = ("thumbnail_","approved",'rejected',"instagram_user","caption")
  list_editable = ("approved",'rejected')
  list_filter = ("approved",'rejected')

admin.site.register(InstagramPhoto,InstagramPhotoAdmin)
admin.site.register(InstagramLocation)
admin.site.register(InstagramTag)
admin.site.register(InstagramUser)
