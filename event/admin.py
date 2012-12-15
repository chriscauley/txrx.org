from django.contrib import admin

from .models import Event, EventOccurence

import datetime

class EventOccurenceInline(admin.TabularInline):
  model = EventOccurence
  fields = ('name_override','start','end')
  def queryset(self,request):
    qs = super(EventOccurenceInline,self).queryset(request)
    return qs.filter(start__gte=datetime.datetime.now())

class EventAdmin(admin.ModelAdmin):
  list_display = ("__unicode__",)
  inlines = [EventOccurenceInline]

admin.site.register(Event,EventAdmin)
admin.site.register(EventOccurence)
