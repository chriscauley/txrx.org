from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template.defaultfilters import slugify, date, urlencode

from wmd import models as wmd_models
from geo.models import Location
from codrspace.models import SetModel

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^wmd\.models\.MarkDownField"])
import simplejson as json
import datetime

def print_time(t):
  if t: return t.strftime('%I:%M %P')
  return ''

class Event(models.Model):
  name = models.CharField(max_length=128,null=True,blank=True)
  _ht = "Optional. Alternative name for the calendar."
  short_name = models.CharField(max_length=64,null=True,blank=True,help_text=_ht)
  location = models.ForeignKey(Location)
  description = wmd_models.MarkDownField(blank=True,null=True)

  get_short_name = lambda self: self.short_name or self.name
  @property
  def upcoming_occurrences(self):
    return self.eventoccurrence_set.filter(start__gte=datetime.datetime.now())

  @property
  def next_occurrence(self):
    if not self.upcoming_occurrences.count():
      return None
    return self.upcoming_occurrences[0]

  def get_name(self):
    return self.name or self.location

  __unicode__ = lambda self: "%s@%s"%(self.name,self.location)
  class Meta:
    pass

class OccurrenceModel(models.Model):
  """
  The goal is to eventually make this very general so that it can reach accross many models to be put into a feed.
  Occurrences need a start (DateTime), end (DateTime, optional), name (str), description (str), and get_absolute_url (str).
  """
  __unicode__ = lambda self: "%s - %s"%(self.name,date(self.start,'l F d, Y'))
  @property
  def google_link(self):
    d = {
      'name': urlencode(self.name),
      'start': date(self.start,"Ymd\THi00\Z"),
      'end': date(self.end,"Ymd\THi00\Z"),
      'description': urlencode(self.description),
      'site_name': urlencode('TX/RX Labs'),
      'location': "205 Roberts Street, Houston TX, 77003",
      'url': 'http://txrxlabs.org/', #+urlencode(self.get_absolute_url()),
      }
    return "http://www.google.com/calendar/event?action=TEMPLATE&text=%(name)s&dates=%(start)s/%(end)s&details=%(description)s&location=%(location)s&trp=false&sprop=%(site_name)s&sprop=name:%(url)s"%d
  class Meta:
    abstract = True

class EventOccurrence(OccurrenceModel,SetModel):
  event = models.ForeignKey(Event)
  start = models.DateTimeField()
  end = models.DateTimeField(null=True,blank=True)
  get_absolute_url = lambda self: reverse('event:occurrence_detail',args=(self.id,slugify(self.name)))
  name_override = models.CharField(null=True,blank=True,max_length=128)
  name = property(lambda self: self.name_override or self.event.name)
  short_name = property(lambda self: self.name_override or self.event.get_short_name())
  description_override = wmd_models.MarkDownField(blank=True,null=True)
  description = property(lambda self: self.description_override or self.event.description)
  class Meta:
    ordering = ('start',)

from .signals import *
