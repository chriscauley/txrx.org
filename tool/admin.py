from django import forms
from django.contrib import admin
from models import Lab, Tool, ToolLink
from db.admin import SlugModelAdmin,OrderedModelAdmin

class LabAdmin(SlugModelAdmin):
  list_display = ("__unicode__","order")
  list_editable = ("order",)

class ToolLinkInline(admin.TabularInline):
  extra = 0
  model = ToolLink
  fields = ("title","url","order")

class ToolAdmin(SlugModelAdmin,OrderedModelAdmin):
  inlines = (ToolLinkInline,)

admin.site.register(Lab,LabAdmin)
admin.site.register(Tool,ToolAdmin)
