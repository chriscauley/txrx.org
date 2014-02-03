from django.contrib import admin
from .models import Thing, Material

from codrspace.admin import TaggedPhotoInline
from tool.admin import TaggedToolInline

class ThingAdmin(admin.ModelAdmin):
  inlines = [TaggedPhotoInline,TaggedToolInline]
  raw_id_fields = ('user',)
  list_display = ('title','active','featured')
  list_editable = ('active','featured')

admin.site.register(Thing,ThingAdmin)
admin.site.register(Material)
