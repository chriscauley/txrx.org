from django.conf import settings
from django.contrib import admin, messages
from django.utils import timezone

from .models import Follow, Notification
from lablackey.db.admin import RawMixin

class NotificationInline(admin.TabularInline):
  model = Notification
  has_add_permission = lambda *args: False
  extra = 0
  readonly_fields = ('user','follow','emailed','message','data','url','target_type','target_id','relationship')

@admin.register(Follow)
class FollowAdmin(RawMixin,admin.ModelAdmin):
  list_display = ("__unicode__",'content_type','notification_count')
  list_filter = ("content_type",)
  raw_id_fields = ('user','content_type')
  inlines = [NotificationInline]
  search_fields = getattr(settings,"USER_SEARCH_FIELDS",[])
  def notification_count(self,obj):
    return obj.notification_set.count()

def mark_emailed(model_admin,request,queryset):
  messages.success(request,"Marked %s notifications as emailed"%queryset.filter(emailed__isnull=True).count())
  for obj in queryset:
    obj.emailed = obj.emailed or timezone.now()
    obj.save()

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
  raw_id_fields = ('user','follow')
  list_display = ("__unicode__","target_type","emailed","read")
  actions = [mark_emailed]
  list_filter = ("target_type",)
