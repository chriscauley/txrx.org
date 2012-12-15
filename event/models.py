from django.db import models
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

  def get_name(self):
    return self.name or self.location

  __unicode__ = lambda self: "%s@%s"%(self.name,self.location)
  class Meta:
    pass

class OccurenceModel(models.Model):
  """
  The goal is to eventually make this very general so that it can reach accross many models to be put into a feed.
  Occurences need a start (DateTime), end (DateTime, optional), name (str), description (str), and get_absolute_url (str).
  """
  start = models.DateTimeField()
  end = models.DateTimeField(null=True,blank=True)
  name_override = models.CharField(null=True,blank=True,max_length=128)
  name = property(lambda self: self.name_override or self.event.name)
  description_override = wmd_models.MarkDownField(blank=True,null=True)
  description = property(lambda self: self.description_override or self.event.description)
  class Meta:
    abstract = True

class EventOccurence(OccurenceModel):
  event = models.ForeignKey(Event)
