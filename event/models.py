from django.db import models
from django.db.utils import ProgrammingError
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.template.defaultfilters import slugify, date, urlencode

from geo.models import Room
from media.models import PhotosMixin
from lablackey.contenttypes import get_contenttype
from lablackey.db.models import UserModel
from lablackey.decorators import cached_property, cached_method
from lablackey.unrest import JsonMixin
from tool.models import CriterionModel
from wmd import models as wmd_models

from dateutil import tz
import datetime, sys, math, arrow, six, calendar

def print_time(t):
  if t: return t.strftime('%I:%M %P')
  return ''

def reverse_ics(obj):
  """ see event.views.ics for information on what objects can be used with this function """
  clss = obj.__class__
  module = clss.__module__.split(".")[0]
  model_str = clss.__name__
  f_name = '%s-%s.ics'%(slugify(obj.name),slugify(settings.SITE_NAME))
  return "%s/event/ics/%s/%s/%s/%s"%(settings.SITE_DOMAIN,module,model_str,obj.id,f_name)

class Access(models.Model):
  name = models.CharField(max_length=32)
  _ht = "The CSS class that styles this. Also used for sorting."
  icon = models.CharField(max_length=16,help_text=_ht)
  order = models.IntegerField(default=999)
  __unicode__ = lambda self: self.name
  class Meta:
    ordering = ("order",)

class Event(PhotosMixin,models.Model):
  _use_default_photo = True
  name = models.CharField(max_length=128,null=True,blank=True)
  url = models.CharField(max_length=256,null=True,blank=True)
  _ht = "Optional. Alternative name for the calendar."
  short_name = models.CharField(max_length=64,null=True,blank=True,help_text=_ht)
  room = models.ForeignKey(Room,null=True,blank=True) #! remove ntbt when you remove location.
  get_room = lambda self: self.room
  description = wmd_models.MarkDownField(blank=True,null=True)
  _ht = "If true, this class will not raise conflict warnings for events in the same room."
  no_conflict = models.BooleanField(default=False,help_text=_ht)
  _ht = "Hidden events won't appear on the calendar."
  hidden = models.BooleanField(default=False,help_text=_ht)
  allow_rsvp = models.BooleanField(default=False)
  _ht = "Number of days before event when RSVP is cut off (eg 0.5 means \"You must rsvp 12 hours before this event\")"
  rsvp_cutoff = models.FloatField(default=0,help_text=_ht)
  max_rsvp = models.IntegerField(default=128)
  access = models.ForeignKey(Access)
  owner_ids = property(lambda self: list(self.eventowner_set.all().values_list("user_id",flat=True)))
  @property
  def non_custom_repeats(self):
    return self.eventrepeat_set.exclude(repeat_flavor="custom")
  @property
  def verbose_rsvp_cutoff(self):
    if self.rsvp_cutoff > 2:
      s = "{} days".format(int(self.rsvp_cutoff))
    else:
      s = "{} hours".format(int(math.ceil(12*self.rsvp_cutoff)))
    return "You must RSVP for this event at least {} before the event begins.".format(s)

  get_short_name = lambda self: self.short_name or self.name
  def get_absolute_url(self):
    return reverse("event:event_detail",args=[self.pk,slugify(self.name)])
  @property
  def all_occurrences(self):
    return self.eventoccurrence_set.all()
  @property
  def upcoming_occurrences(self):
    return self.eventoccurrence_set.filter(start__gte=datetime.datetime.now()-datetime.timedelta(0.5))

  @property
  def next_occurrence(self):
    if not self.upcoming_occurrences.count():
      return None
    return self.upcoming_occurrences[0]
  def get_user_rsvps(self,user,**kwargs):
    occurrence_ids = self.all_occurrences.values_list('id',flat=True)
    rsvps = RSVP.objects.filter(
      user=user,
      object_id__in=occurrence_ids,
      content_type_id=get_contenttype("event.eventoccurrence").id,
      **kwargs
    )
    return {r.object_id:r.quantity for r in rsvps}
  def get_name(self):
    return self.name or self.room

  get_ics_url = lambda self: reverse_ics(self)

  __unicode__ = lambda self: "%s@%s"%(self.name,self.room)
  class Meta:
    pass

REPEAT_FLAVOR_CHOICES = (
  ('start-month','Monthly from start of month (eg, 1st, 2nd... Friday of month)'),
  ('end-month','Monthly from end of month (eg, second to last friday of month'),
  ('weekly','Every Week'),
  ('custom','Custom'),
  #('monthly','Same day (eg 1-31) of ever month'),
)

REPEAT_VERBOSE = {
  'start-month': "The {self.verbose_startweek} {self.verbose_weekday} of every month.",
  'end-month': "The {self.verbose_endweek} {self.verbose_weekday} of every month.",
  'weekly': 'Every {self.verbose_weekday}',
  'custom': 'Custom',
}

class EventOwner(UserModel):
  event = models.ForeignKey(Event)
  __unicode__ = lambda self: "%s owns %s"%(self.user,self.event)

class EventRepeat(JsonMixin,models.Model):
  event = models.ForeignKey(Event)
  repeat_flavor = models.CharField(max_length=16,choices=REPEAT_FLAVOR_CHOICES)
  first_date = models.DateField()
  start_time = models.TimeField()
  end_time = models.TimeField()

  monthcalendar = property(lambda s: calendar.monthcalendar(int(s.first_date.year),int(s.first_date.month)))
  __unicode__ = lambda self: "EventRepeat: %s - %s"%(self.event,self.verbose)
  json_fields = ['event_id','first_date','start_time','end_time','event_name']
  event_name = property(lambda self: unicode(self.event))
  @property
  def month_occurrences(self):
    return self.eventoccurrence_set.filter(start__gte=datetime.datetime.now().replace(day=1,hour=0,minute=0))
  @cached_property
  def startweek(self):
    monthcalendar = self.monthcalendar
    for i in range(len(monthcalendar)):
      if self.first_date.day in monthcalendar[i]:
        dow = monthcalendar[i].index(self.first_date.day)
        if monthcalendar[0][dow]:
          return i
        else: # first week doesn't have that day of week (eg no sunday on first week)
          return i-1
  @cached_property
  def endweek(self):
    monthcalendar = self.monthcalendar
    for i in range(1,len(monthcalendar)):
      if self.first_date.day in monthcalendar[-i]:
        return -i
  @property
  def verbose_startweek(self):
    if self.startweek == 0:
      return "1st"
    if self.startweek == 1:
      return "2nd"
    if self.startweek == 2:
      return "3rd"
    if self.startweek == 3:
      return "4th"
    return self.startweek
  @property
  def verbose_endweek(self):
    if self.endweek == -1:
      return "last"
    if self.endweek == -2:
      return "second to last"
    if self.endweek == -3:
      return "third to last"

  isoweekday = property(lambda self: arrow.get(self.first_date).isoweekday())
  verbose_weekday = property(lambda self: arrow.get(self.first_date).format("dddd"))
  @property
  def verbose(self):
    if self.repeat_flavor:
      return REPEAT_VERBOSE[self.repeat_flavor].format(self=self)
  def generate(self,start_datetime=None,end_date=None):
    if self.repeat_flavor == "custom":
      return
    if not start_datetime:
      # we're going to make these two months out so they can be overridden that far ahead
      start_datetime = timezone.now() + datetime.timedelta(60)
    if not end_date:
      end_date = start_datetime.date() + datetime.timedelta(60)

    last_date = arrow.get(start_datetime.date())
    new_dates = []
    out = []
    # isoweekday means sunday is 7, monday is 1
    week_index = self.isoweekday - 1
    while last_date < arrow.get(end_date):
      monthcalendar = calendar.monthcalendar(last_date.year,last_date.month)
      if self.repeat_flavor == 'start-month':
        week_number = self.startweek if monthcalendar[0][week_index] else self.startweek + 1
        day = monthcalendar[week_number][week_index]
        new_dates.append(datetime.date(last_date.year,last_date.month,day))
      if self.repeat_flavor == 'end-month':
        week_number = self.endweek if monthcalendar[-1][week_index] else self.endweek - 1
        day = monthcalendar[week_number][week_index]
        new_dates.append(datetime.date(last_date.year,last_date.month,day))
      if self.repeat_flavor == 'weekly':
        for week in monthcalendar:
          if week[week_index]:
            new_dates.append(datetime.date(last_date.year,last_date.month,week[week_index]))
      last_date = last_date.replace(months=1)
    for new_date in new_dates:
      if new_date < start_datetime.date():
        continue
      defaults = {
        'end_time': self.end_time,
      }
      start_dt = arrow.get(new_date,tz.gettz(settings.TIME_ZONE))
      start_dt = start_dt.replace(hour=self.start_time.hour,minute=self.start_time.minute).datetime
      occ, new = self.eventoccurrence_set.get_or_create(
        event=self.event,
        eventrepeat=self,
        start=start_dt,
        defaults=defaults
      )
      out.append(occ)
    return out
  def save(self,*args,**kwargs):
    new = not self.pk
    super(EventRepeat,self).save(*args,**kwargs)
    if new:
      self.generate(datetime.datetime.now())
      if self.repeat_flavor == "custom":
        fd = self.first_date
        s = self.start_time
        self.eventoccurrence_set.get_or_create(
          event=self.event,
          eventrepeat=self,
          start=datetime.datetime(fd.year,fd.month,fd.day,s.hour,s.minute),
          end_time=self.end_time,
        )

class OccurrenceModel(models.Model):
  """
  The goal is to eventually make this very general so that it can reach accross many models to be put into a feed.
  Occurrences need a start (DateTime), end (DateTime, optional), name (str), description (str), and get_absolute_url (str).
  """
  start = models.DateTimeField()
  end_time = models.TimeField()
  __unicode__ = lambda self: "%s - %s"%(self.name,date(self.start,'l F d, Y'))
  created = models.DateTimeField(auto_now_add=True)

  get_ics_url = lambda self: reverse_ics(self)

  @property
  def verbose_start(self):
    today = datetime.date.today()
    if self.start.date() == today:
      return "Today"
    if self.start.date() == today +datetime.timedelta(1):
      return "Tomorrow"
    return date(self.start,"D n/j")
  @property
  def end(self):
    return self.start.replace(hour=self.end_time.hour,minute=self.end_time.minute)
  @property
  def google_link(self):
    d = {
      'name': urlencode(self.name),
      'start': date(self.start,"Ymd\THi00"),
      'end': date(self.end,"Ymd\THi00"),
      'description': urlencode(self.description),
      'site_name': settings.SITE_NAME,
      'location': "205 Roberts Street, Houston TX, 77003",
      'url': 'http://txrxlabs.org/', #+urlencode(self.get_absolute_url()),
      }
    return "http://www.google.com/calendar/event?action=TEMPLATE&text=%(name)s&dates=%(start)s/%(end)s&details=%(description)s&location=%(location)s&trp=false&sprop=%(site_name)s&sprop=name:%(url)s"%d
  @property
  def is_external(self):
    url = self.get_absolute_url()
    return not (url.startswith('/') or url.startswith(settings.SITE_URL))
  @property
  def class_name(self):
    return self.icon + (" fa fa-external-link" if self.is_external else "")
  class Meta:
    abstract = True

class RSVPManager(models.Manager):
  def user_controls(self,user,*args,**kwargs):
    event_ids = Event.objects.filter(eventowner__user=user).values_list("id",flat=True)
    eventoccurrence_ids = EventOccurrence.objects.filter(event_id__in=event_ids).values_list("id",flat=True)
    qs = self.filter(content_type=get_contenttype("event.EventOccurrence"),object_id__in=eventoccurrence_ids)
    return qs.filter(*args,**kwargs)

class RSVP(CriterionModel):
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  content_type = models.ForeignKey("contenttypes.ContentType")
  object_id = models.IntegerField()
  content_object = GenericForeignKey('content_type', 'object_id')
  emailed = models.DateTimeField(null=True,blank=True)
  quantity = models.IntegerField(default=0)
  get_occurrences = lambda self: [self.content_object]
  objects = RSVPManager()
  __unicode__ = lambda self: "%s for %s"%(self.user,self.content_object)
  def get_criteria(self):
    return self.content_object.event.criterion_set.all()

class EventOccurrence(PhotosMixin,OccurrenceModel):
  event = models.ForeignKey(Event)
  eventrepeat = models.ForeignKey(EventRepeat,models.SET_NULL,null=True,blank=True) # for when eventrepeat changes
  publish_dt = models.DateTimeField(default=datetime.datetime.now) # for rss feed
  get_admin_url = lambda self: "/admin/event/event/%s/"%self.event.id
  name_override = models.CharField(null=True,blank=True,max_length=128)
  name = property(lambda self: self.name_override or self.event.name)
  short_name = property(lambda self: self.name_override or self.event.get_short_name())
  url = property(lambda self: self.url_override or self.event.url)
  description_override = wmd_models.MarkDownField(blank=True,null=True)
  description = property(lambda self: self.description_override or self.event.description)
  get_room = lambda self: self.event.room #! depracate me
  room = cached_property(lambda self: self.event.room,name="room")
  no_conflict = property(lambda self: self.event.no_conflict)

  url_override = models.CharField(max_length=256,null=True,blank=True)
  #_get_absolute_url = lambda self: reverse('event:occurrence_detail',args=(self.id,slugify(self.name)))
  @cached_method
  def get_absolute_url(self):
    return self.url_override or self.event.url or self.event.get_absolute_url()

  rsvp_cutoff = property(lambda self: self.end - datetime.timedelta(self.event.rsvp_cutoff))
  total_rsvp = property(lambda self: sum([r.quantity for r in self.get_rsvps()]))
  full = property(lambda self: self.total_rsvp >= self.event.max_rsvp)
  icon = property(lambda self: self.event.access.icon)
  try:
    _cid = ContentType.objects.get(model="eventoccurrence").id
  except ProgrammingError:
    pass # this breaks on the initial migration
  @cached_method
  def get_rsvps(self):
    return RSVP.objects.filter(object_id=self.id,content_type_id=self._cid)
  def save(self,*args,**kwargs):
    # set the publish_dt to a week before the event
    self.publish_dt = self.start - datetime.timedelta(7)
    super(EventOccurrence,self).save(*args,**kwargs)
  @property
  def past(self):
    now = datetime.datetime.now()
    return (self.end < now) or (self.rsvp_cutoff < now and not self.get_rsvps().count())
  @property
  def as_json(self):
    return {
      'room_id': self.event.room_id,
      'name': self.name,
      'start': str(self.start),
      'end': str(self.end),
    }
  class Meta:
    ordering = ('start',)

class CheckInPoint(models.Model):
  room = models.ForeignKey(Room)
  __unicode__ = lambda self: "%s"%self.room
  class Meta:
    ordering = ('room__name',)

class CheckIn(UserModel):
  datetime = models.DateTimeField(auto_now_add=True)
  object_id = models.IntegerField(null=True,blank=True)
  content_type = models.ForeignKey("contenttypes.ContentType",null=True,blank=True)
  content_object = GenericForeignKey('content_type', 'object_id')
  checkinpoint = models.ForeignKey(CheckInPoint)
  __unicode__ = lambda self: "%s @ %s - %s"%(self.user,self.checkinpoint,self.datetime)
  class Meta:
    ordering = ('-datetime',)
