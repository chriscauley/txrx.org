from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Consumable, Category, ToolConsumableGroup
from lablackey.db.admin import NamedTreeModelAdmin
from media.admin import TaggedPhotoAdmin

@admin.register(ToolConsumableGroup)
class ToolConsumableGroupAdmin(admin.ModelAdmin):
  filter_horizontal = ('tools','consumables')

@admin.register(Category)
class CategoryAdmin(NamedTreeModelAdmin):
  pass

@admin.register(Consumable)
class ConsumableAdmin(TaggedPhotoAdmin):
  list_display = ('__unicode__','in_stock','unit_price','_status')
  list_filter = ('categories',)
  exclude = ('slug',)
  def _status(self,obj=None):
    out = ''
    if obj.purchase_url:
      out += "<a href='%s' class='btn btn-success'>%s</a>"%(obj.purchase_url,obj.purchase_domain)
    else:
      out += "<a class='btn btn-danger'>No Domain</a>"
    if not obj.get_photos():
      out += "<a class='btn btn-danger'>No Photo</a>"
    return out
  _status.allow_tags = True
