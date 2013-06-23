from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import USStateField
from .widgets import LocationField

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
    verbose_name_plural = "Cities"

class Location(GeoModel):
  name = models.CharField(max_length=128,null=True,blank=True)
  address = models.CharField(max_length=64,null=True,blank=True)
  address2 = models.CharField(max_length=64,null=True,blank=True)
  city = models.ForeignKey(City,default=1)
  zip_code = models.IntegerField(default=77007)

  def print_address(self):
    l = [self.name,self.address,self.address2,self.city.__unicode__(),self.zip_code]
    return '\n'.join([str(li) for li in l if li])
  def __unicode__(self):
    items = [self.name, self.address, self.address2, self.city, self.zip_code]
    return ', '.join([str(i) for i in items if i])
