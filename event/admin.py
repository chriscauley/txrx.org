from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from django.core.urlresolvers import reverse

from .models import Event, EventOccurrence
from codrspace.admin import PhotoSetConnectionInline

import datetime

class EventOccurrenceInline(admin.TabularInline):
  model = EventOccurrence
  fields = ('name_override','start','end','_photoset')
  readonly_fields = ['_photoset']
  def queryset(self,request):
    qs = super(EventOccurrenceInline,self).queryset(request)
    return qs.filter(start__gte=datetime.datetime.now())
  def _photoset(self,obj):
    return '<a href="/admin/event/edit_photoset/%s/">Edit Photo Set</a>'%obj.id
  _photoset.allow_tags = True

class EventAdmin(admin.ModelAdmin):
  list_display = ("__unicode__","repeat")
  inlines = [EventOccurrenceInline]

class EventOccurrenceAdmin(admin.ModelAdmin):
  inlines = [PhotoSetConnectionInline]

admin.site.register(Event,EventAdmin)
admin.site.register(EventOccurrence,EventOccurrenceAdmin)
