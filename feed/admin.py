from django.contrib import admin
from .models import FeedItem, Thing, Material

from codrspace.admin import TaggedPhotoInline
from tool.admin import TaggedToolInline

class FeedItemAdmin(admin.ModelAdmin):
  pass

class ThingAdmin(admin.ModelAdmin):
  inlines = [TaggedPhotoInline,TaggedToolInline]
  raw_id_fields = ('user',)

admin.site.register(FeedItem,FeedItemAdmin)
admin.site.register(Thing,ThingAdmin)
admin.site.register(Material)
