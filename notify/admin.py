from django.contrib import admin

from .models import NotifyCourse

class NotifyCourseAdmin(admin.ModelAdmin):
  list_display = ("__unicode__","_enrolled")
  raw_id_fields = ("user","course",)
  def _enrolled(self,obj):
    return obj.user.enrollment_set.filter(session__section__course=obj.course).count()

admin.site.register(NotifyCourse,NotifyCourseAdmin)
