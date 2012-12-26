from django.contrib import admin
from crop_override.admin import CropAdmin

from .models import Post, Media

class PostAdmin(admin.ModelAdmin):
  list_display = ('__unicode__','author','featured','publish_dt','status')
  list_editable = ('featured','status')

class MediaAdmin(CropAdmin):
  pass

admin.site.register(Post,PostAdmin)
admin.site.register(Media,MediaAdmin)
