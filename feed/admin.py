from django.contrib import admin
from .models import FeedItem

class FeedItemAdmin(admin.ModelAdmin):
  pass
admin.site.register(FeedItem,FeedItemAdmin)
