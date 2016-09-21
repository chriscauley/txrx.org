from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth import get_user_model

from media.admin import TaggedPhotoInline
from lablackey.db.admin import OrderedModelAdmin
from event.admin import FuturePastListFilter
from .models import (Lab, Tool, ToolLink, TaggedTool, Group, Permission, Criterion, UserCriterion, APIKey,
                     Schedule, ScheduleDay, PermissionSchedule, DoorGroup, Holiday)
from store.admin import TaggedConsumableInline

#@admin.register(APIKey)
#class APIKeyAdmin(admin.ModelAdmin):
#  readonly_fields = ['key']

@admin.register(DoorGroup)
class DoorGroupAdmin(admin.ModelAdmin):
  pass

class ScheduleDayInline(admin.TabularInline):
  model = ScheduleDay
  extra = 0
  def has_add_permission(self,request):
    return not request.path.endswith("/add/")

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
  inlines = [ScheduleDayInline]
  readonly_fields = ['instructions']
  def get_readonly_fields(self,request,obj=None):
    if obj and obj.pk:
      return []
    return super(ScheduleAdmin,self).get_readonly_fields(request,obj)
  def get_inline_instances(self, request, obj=None):
    if not obj or not obj.pk:
      return []
    return super(ScheduleAdmin,self).get_inline_instances(request,obj)
  def instructions(self,obj=None):
    if not obj or not obj.pk:
      return "Save and continue editing and a template will be made off with every day set at 10am-10pm."

class FuturePastListFilter(FuturePastListFilter):
  filter_field = 'date'

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
  list_filter = [FuturePastListFilter]

@admin.register(Lab)
class LabAdmin(OrderedModelAdmin):
  inlines = (TaggedPhotoInline,)
  raw_id_fields = ('photo',)

class ToolLinkInline(admin.TabularInline):
  extra = 0
  model = ToolLink
  fields = ("title","url","order")

@admin.register(Tool)
class ToolAdmin(OrderedModelAdmin):
  inlines = (ToolLinkInline,TaggedPhotoInline,TaggedConsumableInline)
  list_display = ('__unicode__','has_links','has_description','_materials',"room","lab",'order','permission')
  list_filter = ('lab','functional')
  filter_horizontal = ('materials',)
  list_editable = ('permission',)
  readonly_fields = ('has_links','has_description')
  def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == "permission":
      kwargs["queryset"] = Permission.objects.all().order_by("name")
    return super(ToolAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
  def has_links(self,obj):
    return bool(obj.links())
  has_links.boolean = True
  def has_description(self,obj):
    return bool(obj.description)
  has_description.boolean = True
  def _materials(self,obj):
    m = obj.materials
    if not m.count():
      return'<img src="/static/admin/img/icon-no.gif" alt="False">'
    return "%s (%s)"%(m.filter(parent__isnull=True).count(),m.filter(parent__isnull=False).count())
  _materials.allow_tags = True

#See note above corresponding model
class TaggedToolInline(GenericTabularInline):
  model = TaggedTool
  raw_id_fields = ('tool',)
  extra = 0

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
  list_display = ('__unicode__','row','column','color')
  list_editable = ('row','column','color')

class PermissionScheduleInline(admin.TabularInline):
  model = PermissionSchedule
  extra = 0

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
  filter_horizontal = ('criteria',)
  list_editable = ('group',"order",)
  list_display = ('__unicode__','abbreviation','group','order','_criteria')
  fields = (('name','abbreviation'),('group','room'),'criteria','_schedule_helptext')
  readonly_fields = ('_schedule_helptext',)
  _criteria = lambda self,obj: '<br/>'.join([unicode(criteria) for criteria in obj.criteria.all()])
  _criteria.allow_tags = True
  _criteria.short_description = "Required Criteria"
  inlines = [PermissionScheduleInline]
  def _schedule_helptext(request,obj):
    _s = 'Tool access will default to buisness hours for hackers and above and weekends only for tinkerers '\
         ' if no schedules specified below.'
    return '<p class="lead">%s</p>'%_s
  _schedule_helptext.allow_tags = True

@admin.register(Criterion)
class CriterionAdmin(admin.ModelAdmin):
  filter_horizontal = ("courses",)

@admin.register(UserCriterion)
class UserCriterionAdmin(admin.ModelAdmin):
  raw_id_fields = ('user',)
  readonly_fields = ("content_type","object_id",'criterion')
