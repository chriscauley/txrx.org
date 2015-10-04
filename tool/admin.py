from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from media.admin import TaggedPhotoInline
from lablackey.db.admin import OrderedModelAdmin
from .models import Lab, Tool, ToolLink, TaggedTool, Permission
from course.models import CoursePermission

class LabAdmin(OrderedModelAdmin):
  inlines = (TaggedPhotoInline,)
  raw_id_fields = ('photo',)

class ToolLinkInline(admin.TabularInline):
  extra = 0
  model = ToolLink
  fields = ("title","url","order")

class ToolAdmin(OrderedModelAdmin):
  inlines = (ToolLinkInline,TaggedPhotoInline)
  list_display = ('__unicode__','has_links','has_description','_materials','make','model',"lab",'order')
  list_filter = ('lab','functional')
  filter_horizontal = ('materials',)
  readonly_fields = ('has_links','has_description')
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

class CoursePermissionInline(admin.TabularInline):
  model = CoursePermission
  raw_id_fields = ('course',)
  extra = 0

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
  filter_horizontal = ('tools',)
  inlines = [CoursePermissionInline]

admin.site.register(Lab,LabAdmin)
admin.site.register(Tool,ToolAdmin)
