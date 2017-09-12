from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Consumable, ToolConsumableGroup, CourseCheckout
from lablackey.db.admin import NamedTreeModelAdmin
from media.admin import TaggedPhotoAdmin

@admin.register(CourseCheckout)
class CourseCheckoutAdmin(admin.ModelAdmin):
  list_display = ("__unicode__","course","event")
  list_editable = ("course","event")
  raw_id_fields = ("course",)

@admin.register(ToolConsumableGroup)
class ToolConsumableGroupAdmin(admin.ModelAdmin):
  filter_horizontal = ('tools','consumables')

@admin.register(Consumable)
class ConsumableAdmin(TaggedPhotoAdmin):
  list_display = ('__unicode__','in_stock','unit_price','_status')
  #list_filter = ('categories',)
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
