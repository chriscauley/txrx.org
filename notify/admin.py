from django.contrib import admin

from .models import Follow, Notification
from lablackey.db.admin import RawMixin

@admin.register(Follow)
class FollowAdmin(RawMixin,admin.ModelAdmin):
  list_display = ("__unicode__",)
