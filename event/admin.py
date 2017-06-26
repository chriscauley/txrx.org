from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.forms.models import BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _

from .models import Event, EventRepeat, EventOccurrence, RSVP, CheckIn, CheckInPoint, Access, EventOwner
from event.utils import get_room_conflicts, get_person_conflicts
from lablackey.db.admin import RawMixin
from media.admin import TaggedPhotoAdmin

import datetime,functools

@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
  pass

@admin.register(CheckInPoint)
class CheckInPointAdmin(admin.ModelAdmin):
  pass

def message_conflicts(request,obj,room_conflicts,user_conflicts):
  if not (room_conflicts or user_conflicts):
    return
  f1 = "%b %-d "
  f2 = "%-I:%M %p"
  messages.error(request,"%s was saved, but there are conflicts!"%obj)
  messages.error(request,"Checkout /admin/ for an easy interface linking to all conflicts")
  for room,conflict_tuples in room_conflicts:
    for (start,end),events in conflict_tuples:
      for event in events:
        if event != obj:
          t = (event.name,room,start.strftime(f1+f2),end.strftime(f2))
          m = "%s is in the same room (%s) with overlapping time %s-%s"%t
          messages.error(request,m)
  for user,start,end,occurrences in user_conflicts:
    for occurrence in occurrences:
      if occurrence != obj:
        t = (user,occurrence.name,start.strftime(f1+f2),end.strftime(f2))
        m = "User %s is also scheduled for %s with overlapping time %s to %s"%t
        messages.error(request,m)

def check_conflicts(request,obj):
  room_conflicts = get_room_conflicts(obj)
  user_conflicts = []
  for eventowner in obj.event.eventowner_set.all():
    user = eventowner.user
    user_conflicts += get_person_conflicts(user,obj)
  message_conflicts(request,obj,room_conflicts,user_conflicts)

def mark_conflicts(request,obj):
  request.session['conflicts'] = request.session.get('conflicts', [])
  meta = obj.__class__._meta
  request.session['conflicts'].append([meta.app_label,meta.model_name, obj.pk])

class OccurrenceModelFormSet(BaseInlineFormSet):
  def save_existing(self, form, obj, commit=True):
    obj = super(OccurrenceModelFormSet,self).save_existing(form,obj,commit=commit)
    mark_conflicts(obj)
    return obj
  def save_new(self, form, commit=True):
    obj = super(OccurrenceModelFormSet,self).save_new(form,commit=commit)
    mark_conflicts(self.request,obj)
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
  readonly_fields = ['_verbose',]
  extra = 0
  def _verbose(self,obj):
    if obj.repeat_flavor == "custom":
      return "<a href='/event/bulk/?eventrepeat_id=%s' class='fa fa-edit'></a>"%obj.id
    return obj.verbose
  _verbose.allow_tags = True

class EventOwnerInline(admin.TabularInline):
  raw_id_fields = ['user']
  extra = 0
  model = EventOwner

@admin.register(Event)
class EventAdmin(TaggedPhotoAdmin):
  list_display = ("__unicode__","upcoming_count","organizers","get_repeat_verbose","access","allow_rsvp","rsvp_cutoff")
  list_editable = ("access","allow_rsvp","rsvp_cutoff")
  list_filter = ("allow_rsvp","access")
  inlines = [EventRepeatInline,EventOwnerInline,EventOccurrenceInline]
  search_fields = ['name']
  def organizers(self,obj):
    return "<br />".join(["%s"%eo.user for eo in obj.eventowner_set.all()])
  organizers.allow_tags = True
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
  def save_model(self,request,obj,form,change):
    super(EventOccurrenceAdmin,self).save_model(request,obj,form,change)
    mark_conflicts(request,obj)
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
