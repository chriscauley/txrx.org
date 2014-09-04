from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from django.core.urlresolvers import reverse

from .models import Event, EventOccurrence
from media.admin import TaggedPhotoInline

import datetime

class EventOccurrenceInline(admin.TabularInline):
  model = EventOccurrence
  fields = ('name_override','start','end_time')
  def queryset(self,request):
    qs = super(EventOccurrenceInline,self).queryset(request)
    return qs.filter(start__gte=datetime.datetime.now())

class EventAdmin(admin.ModelAdmin):
  list_display = ("__unicode__","repeat")
  inlines = [EventOccurrenceInline,TaggedPhotoInline]

class EventOccurrenceAdmin(admin.ModelAdmin):
  inlines = [TaggedPhotoInline]

admin.site.register(Event,EventAdmin)
admin.site.register(EventOccurrence,EventOccurrenceAdmin)
