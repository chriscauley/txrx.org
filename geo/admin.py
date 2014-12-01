from django.contrib import admin
from .models import City,Location, Room

class LocationAdmin(admin.ModelAdmin):
  fields = ('name','short_name','parent','address','address2','city','zip_code','latlon','dxf','src')

admin.site.register(Room)
admin.site.register(City)
admin.site.register(Location,LocationAdmin)
