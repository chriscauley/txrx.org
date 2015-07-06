from django.contrib import admin
from .models import Thing, Material

from db.admin import NamedTreeModelAdmin
from media.admin import TaggedPhotoAdmin, TaggedFileInline
from tool.admin import TaggedToolInline

class ThingAdmin(TaggedPhotoAdmin):
  inlines = [TaggedToolInline, TaggedFileInline]
  raw_id_fields = ('user','parent','session')
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
admin.site.register(Material,NamedTreeModelAdmin)
