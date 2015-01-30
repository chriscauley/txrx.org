from django.contrib import admin
from .models import City, Location, Room, DXFEntity, RoomGroup

class LocationAdmin(admin.ModelAdmin):
  fields = ('name','short_name','parent','address','address2','city','zip_code','latlon','dxf')

class RoomAdmin(admin.ModelAdmin):
  list_display = ('__unicode__','roomgroup')
  list_editable = ('roomgroup',)

class DXFEntityAdmin(admin.ModelAdmin):
  list_display = ('__unicode__','room')
  list_editable = ('room',)

admin.site.register(Room,RoomAdmin)
admin.site.register(City)
admin.site.register(RoomGroup)
admin.site.register(DXFEntity,DXFEntityAdmin)
admin.site.register(Location,LocationAdmin)
