from django.contrib import admin
from django.core.urlresolvers import reverse

from .models import Event, EventOccurrence

import datetime

class EventOccurrenceInline(admin.TabularInline):
  model = EventOccurrence
  fields = ('name_override','start','end')
  def queryset(self,request):
    qs = super(EventOccurrenceInline,self).queryset(request)
    return qs.filter(start__gte=datetime.datetime.now())

class EventAdmin(admin.ModelAdmin):
  list_display = ("__unicode__",)
  inlines = [EventOccurrenceInline]
  readonly_fields = ['_repeat_event']
  def _repeat_event(self,obj):
    if not obj.id:
      return 'Please save all changes before repeating.'
    if not obj.next_occurrence:
      return 'You cannot repeat an event without an upcoming occurrence.'
    l = '<a href="%s">Repeat next occurrence %s for one year</a>'
    lines = ['Please save all changes before repeating.','This will delete all upcoming Event Occurrences and...']
    lines += [l%(reverse('repeat_event',args=(p,obj.id)),p) for p in ('weekly','monthly')]
    return '<br />'.join(lines)
    
  _repeat_event.allow_tags = True

admin.site.register(Event,EventAdmin)
admin.site.register(EventOccurrence)
