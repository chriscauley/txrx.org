from django.contrib import admin, messages
from .models import Tag, Task, Occurrence

class OccurrenceInline(admin.TabularInline):
  model = Occurrence
  fields = ("datetime","complete")

def update_occurrences(modeladmin,request,queryset):
  for obj in queryset:
    obj.update_occurrences()
  messages.success(request,"Occurences for %s Task(s) have been updated"%queryset.count())

class TaskAdmin(admin.ModelAdmin):
  inlines = [OccurrenceInline]
  filter_horizontal = ("tags",)
  actions = [update_occurrences]

class TagAdmin(admin.ModelAdmin):
  exclude = ("slug",)

admin.site.register(Task,TaskAdmin)
admin.site.register(Tag,TagAdmin)
