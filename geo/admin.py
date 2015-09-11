from django.contrib import admin
from lablackey.db.admin import RawMixin
from .models import City, Location, Room, DXFEntity, RoomGroup

class LocationAdmin(admin.ModelAdmin):
  fields = ('name','short_name','parent','address','address2','city','zip_code','latlon','dxf')

class RoomAdmin(admin.ModelAdmin):
  list_display = ('__unicode__','roomgroup','map_key')
  list_editable = ('roomgroup','map_key')

class DXFEntityAdmin(admin.ModelAdmin):
  list_display = ('__unicode__','room')
  list_editable = ('room',)

class RoomGroupAdmin(RawMixin,admin.ModelAdmin):
  raw_id_fields = ('fill',)

admin.site.register(Room,RoomAdmin)
admin.site.register(City)
admin.site.register(RoomGroup,RoomGroupAdmin)
admin.site.register(DXFEntity,DXFEntityAdmin)
admin.site.register(Location,LocationAdmin)
