from django.contrib import admin
from .models import FeedItem, Thing

from codrspace.admin import TaggedPhotoInline

class FeedItemAdmin(admin.ModelAdmin):
  pass

class ThingAdmin(admin.ModelAdmin):
  inlines = [TaggedPhotoInline]

admin.site.register(FeedItem,FeedItemAdmin)
admin.site.register(Thing,ThingAdmin)
