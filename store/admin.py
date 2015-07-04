from django.contrib import admin

from .models import Consumable, Category
from db.admin import NamedTreeModelAdmin
from media.admin import TaggedPhotoAdmin

class CategoryAdmin(NamedTreeModelAdmin):
  pass

class ConsumableAdmin(TaggedPhotoAdmin):
  list_display = ('__unicode__','in_stock','unit_price','_status')
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
admin.site.register(Consumable,ConsumableAdmin)
admin.site.register(Category,NamedTreeModelAdmin)
