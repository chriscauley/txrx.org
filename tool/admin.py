from django import forms
from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline

from codrspace.admin import TaggedPhotoInline
from db.admin import OrderedModelAdmin
from .models import Lab, Tool, ToolLink, TaggedTool

class LabAdmin(OrderedModelAdmin):
  inlines = (TaggedPhotoInline,)
  raw_id_fields = ('photo',)

class ToolLinkInline(admin.TabularInline):
  extra = 0
  model = ToolLink
  fields = ("title","url","order")

class ToolAdmin(OrderedModelAdmin):
  inlines = (ToolLinkInline,TaggedPhotoInline)
  list_display = ('__unicode__','make','model',"lab",'order')
  list_filter = ('lab',)
  filter_horizontal = ('materials',)

#See note above corresponding model
class TaggedToolInline(GenericTabularInline):
  model = TaggedTool
  raw_id_fields = ('tool',)
  extra = 0

admin.site.register(Lab,LabAdmin)
admin.site.register(Tool,ToolAdmin)
