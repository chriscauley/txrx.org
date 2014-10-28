from django.db import models
from django.conf import settings
from localflavor.us.models import USStateField
from .widgets import LocationField

try:
  from south.modelsinspector import add_introspection_rules
  add_introspection_rules([], ["^localflavor\.us\.models\.USStateField"])
except ImportError:
  #necessary if you're going to use south
  pass

class GeoModel(models.Model):
  latlon = LocationField(max_length=500,null=True,blank=True) # stored as lat,lon
  _lat = property(lambda self: float(self.latlon.split(",")[0]))
  _lon = property(lambda self: float(self.latlon.split(",")[1]))
  @property
  def lat(self):
    if self.latlon: return self._lat
    return False
  @property
  def lon(self):
    if self.latlon: return self._lon
    return False
  class Meta:
    abstract = True

class City(GeoModel):
  name = models.CharField(max_length=128)
  state = USStateField()
  def __unicode__(self):
    return "%s, %s"%(self.name,self.state)
  class Meta:
    ordering = ('name',)
    verbose_name_plural = "Cities"

class Location(GeoModel):
  name = models.CharField(max_length=128,null=True,blank=True)
  parent = models.ForeignKey("self",null=True,blank=True)
  _ht = "Optional. Alternative name for the calendar."
  short_name = models.CharField(max_length=64,null=True,blank=True,help_text=_ht)
  get_short_name = lambda self: self.short_name or self.name
  address = models.CharField(max_length=64,null=True,blank=True)
  address2 = models.CharField(max_length=64,null=True,blank=True)
  city = models.ForeignKey(City,default=1)
  zip_code = models.IntegerField(default=77007)
  dxf = models.FileField(upload_to="floorplans",null=True,blank=True)
  src = models.ImageField(upload_to="floorplans",null=True,blank=True)
  __unicode__ = lambda self: self.name
  class Meta:
    ordering = ('name',)

  def print_address(self):
    l = [self.name,self.address,self.address2,self.city.__unicode__(),self.zip_code]
    return '\n'.join([str(li) for li in l if li])

class Room(models.Model):
  name = models.CharField(max_length=128,null=True,blank=True)
  location = models.ForeignKey(Location)
  _ht = "Optional. Alternative name for the calendar."
  short_name = models.CharField(max_length=64,null=True,blank=True,help_text=_ht)
  get_short_name = lambda self: self.short_name or self.name
  geometry = models.CharField(max_length=32,null=True,blank=True)
  def __unicode__(self):
    if self.name:
      return "%s @ %s"%(self.name,self.location)
    return "%s"%self.location
  class Meta:
    ordering = ('name',)
    unique_together = ('name','location')
