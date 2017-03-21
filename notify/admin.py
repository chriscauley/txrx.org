from django.contrib import admin

from .models import Follow, Notification
from lablackey.db.admin import RawMixin

class NotificationInline(admin.TabularInline):
  model = Notification
  has_add_permission = lambda *args: False
  extra = 0
  readonly_fields = ('user','follow','emailed','message','data','url','target_type','target_id','relationship')

@admin.register(Follow)
class FollowAdmin(RawMixin,admin.ModelAdmin):
  list_display = ("__unicode__",)
  inlines = [NotificationInline]
  search_fields = ("user__username","user__email","user__first_name","user__last_name","user__paypal_email")
