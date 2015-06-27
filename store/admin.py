from django.contrib import admin

from .models import Consumable, Category
from db.admin import NamedTreeModelAdmin

class CategoryAdmin(NamedTreeModelAdmin):
  pass

class ConsumableAdmin(admin.ModelAdmin):
  pass

admin.site.register(Consumable,ConsumableAdmin)
admin.site.register(Category,NamedTreeModelAdmin)
