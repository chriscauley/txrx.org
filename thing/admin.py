from django.contrib import admin
from .models import Thing, Material

from codrspace.admin import TaggedPhotoInline
from tool.admin import TaggedToolInline

class ThingAdmin(admin.ModelAdmin):
  inlines = [TaggedPhotoInline,TaggedToolInline]
  raw_id_fields = ('user','parent')
  list_display = ('title','active','featured','_missing')
  list_editable = ('active','featured')
  filter_horizontal = ('materials',)
  def _missing(self,obj):
    out = ''
    if not obj.get_tools():
      out += 'tools '
    if not obj.materials.count():
      out += 'materials'
    return out

admin.site.register(Thing,ThingAdmin)
admin.site.register(Material)
