from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.forms.models import BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _

from .models import Event, EventRepeat, EventOccurrence, RSVP, CheckIn, CheckInPoint, Access, EventOwner
from event.utils import get_room_conflicts
from lablackey.db.admin import RawMixin
from media.admin import TaggedPhotoAdmin

import datetime,functools

@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
  pass

@admin.register(CheckInPoint)
class CheckInPointAdmin(admin.ModelAdmin):
  pass

class OccurrenceModelFormSet(BaseInlineFormSet):
  def check_conflicts(self,obj):
    conflicts = get_room_conflicts(obj)
    if conflicts:
      m = "%s was saved, but some of the times conflict with other events in the room: %s"
      messages.error(self.request,m%(obj,obj.room))
    for room,conflict_tuples in conflicts:
      for (start,end),events in conflict_tuples:
        for event in events:
          if event != obj:
            m = "%s is in the same room with overlapping time %s-%s"%(event,start,end)
            messages.error(self.request,m)
  def save_existing(self, form, obj, commit=True):
    obj = super(OccurrenceModelFormSet,self).save_existing(form,obj,commit=commit)
    self.check_conflicts(obj)
    return obj
  def save_new(self, form, commit=True):
    obj = super(OccurrenceModelFormSet,self).save_new(form,commit=commit)
    self.check_conflicts(obj)
    return obj

class OccurrenceModelInline(admin.TabularInline):
  formset = OccurrenceModelFormSet
  def get_formset(self, request, obj=None, **kwargs):
    form_class = super(OccurrenceModelInline, self).get_formset(request, obj, **kwargs)
    form_class.request = request
    return form_class

class FuturePastListFilter(admin.SimpleListFilter):
  title = _('Filter by Date')
  parameter_name = 'futurepast'
  filter_field = 'start'

  def lookups(self, request, model_admin):
    return (
      ('__gte', _('Hide Past Events')),
      ('__lt', _('Past Events Only')),
    )
    
  def queryset(self, request, queryset):
    return queryset.filter(**{self.filter_field+(self.value() or '__gte'):datetime.date.today()})

class EventOccurrenceInline(OccurrenceModelInline):
  model = EventOccurrence
  fields = ('name_override','start','end_time','url_override','get_repeat_verbose')
  readonly_fields = ('get_repeat_verbose',)
  def get_repeat_verbose(self,obj):
    if obj.eventrepeat:
      return obj.eventrepeat.verbose
  def get_queryset(self,request):
    qs = super(EventOccurrenceInline,self).get_queryset(request)
    return qs.filter(start__gte=datetime.datetime.now())
  extra = 0

class EventRepeatInline(admin.TabularInline):
  model = EventRepeat
  readonly_fields = ['verbose',]
  extra = 0

class EventOwnerInline(admin.TabularInline):
  raw_id_fields = ['user']
  extra = 0
  model = EventOwner

@admin.register(Event)
class EventAdmin(TaggedPhotoAdmin):
  list_display = ("__unicode__","upcoming_count","get_repeat_verbose","access","allow_rsvp","rsvp_cutoff")
  list_editable = ("access","allow_rsvp","rsvp_cutoff")
  inlines = [EventRepeatInline,EventOccurrenceInline,EventOwnerInline]
  search_fields = ['name']
  def upcoming_count(self,obj):
    return obj.upcoming_occurrences.count()
  def get_repeat_verbose(self,obj):
    return "<br/>".join([er.verbose for er in obj.eventrepeat_set.all()])
  get_repeat_verbose.allow_tags = True

@admin.register(EventOccurrence)
class EventOccurrenceAdmin(TaggedPhotoAdmin):
  search_fields = ['event__name']
  raw_id_fields = ['event']
  list_filter = (FuturePastListFilter,)
  readonly_fields = ['_rsvps','eventrepeat']
  def _rsvps(self,obj):
    rsvps = RSVP.objects.filter(
      object_id=obj.id,
      content_type__model=obj._meta.model_name,
      content_type__app_label=obj._meta.app_label
    )
    s = '<a href="/admin/event/rsvp/{r.id}">{r}</a>'
    return '<br/>'.join([s.format(**{'r': r}) for r in rsvps])
  _rsvps.allow_tags = True

@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
  list_display = ['__unicode__','user_link']
  raw_id_fields = ['user']
  def user_link(self,obj):
    u = obj.user
    html = '<a href="/admin/user/user/{}/" class="fa fa-user"> {} {} ({})</a>'
    return html.format(u.id,u.first_name, u.last_name, u.username)
  user_link.allow_tags = True

@admin.register(Access)
class AccessAdmin(admin.ModelAdmin):
  pass
