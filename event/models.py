from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings

from wmd import models as wmd_models
from lablackey.geo.models import Location

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^wmd\.models\.MarkDownField"])
import simplejson as json
import datetime

def print_time(t):
  if t: return t.strftime('%I:%M %P')
  return ''

class Event(models.Model):
  name = models.CharField(max_length=128,null=True,blank=True)
  location = models.ForeignKey(Location)
  description = wmd_models.MarkDownField(blank=True,null=True)

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
  start = models.DateTimeField()
  end = models.DateTimeField(null=True,blank=True)
  name_override = models.CharField(null=True,blank=True,max_length=128)
  name = property(lambda self: self.name_override or self.event.name)
  description_override = wmd_models.MarkDownField(blank=True,null=True)
  description = property(lambda self: self.description_override or self.event.description)
  __unicode__ = lambda self: "%s - %s"%(self.name,self.start)
  class Meta:
    abstract = True
    ordering = ('start',)

class EventOccurrence(OccurrenceModel):
  event = models.ForeignKey(Event)
  get_absolute_url = lambda self: reverse('occurrence_detail',args=(self.id,))
