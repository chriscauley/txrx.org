from django.contrib import admin
from .models import City,Location

class LocationAdmin(admin.ModelAdmin):
  fields = ('name','short_name','parent','address','address2','city','zip_code','latlon')

admin.site.register(City)
admin.site.register(Location,LocationAdmin)
