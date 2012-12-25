from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin

admin.site.unregister(FlatPage)

class FlatPageAdmin(FlatPageAdmin):
  pass

admin.site.register(FlatPage,FlatPageAdmin)
