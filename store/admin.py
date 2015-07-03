from django.contrib import admin

from .models import Consumable, Category
from db.admin import NamedTreeModelAdmin
from media.admin import TaggedPhotoAdmin

class CategoryAdmin(NamedTreeModelAdmin):
  pass

class ConsumableAdmin(TaggedPhotoAdmin):
  list_display = ('__unicode__','in_stock','unit_price')

admin.site.register(Consumable,ConsumableAdmin)
admin.site.register(Category,NamedTreeModelAdmin)
