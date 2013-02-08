from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import datetime

from geo.models import Location

photofile_path = 'uploads/instagram'

class InstagramLocation(models.Model):
  name = models.CharField(max_length=128)
  latitude = models.FloatField()
  longitude = models.FloatField()
  iid = models.CharField(max_length=32) #instagram id!
  __unicode__ = lambda self: "Instagram Location: %s"%self.name

class InstagramPhoto(models.Model):
  thumbnail = models.ImageField(upload_to=photofile_path,null=True,blank=True)
  low_resolution = models.ImageField(upload_to=photofile_path,null=True,blank=True)
  standard_resolution = models.ImageField(upload_to=photofile_path,null=True,blank=True)
  username = models.CharField(max_length=50)
  user = models.ForeignKey(User,null=True,blank=True)
  caption = models.CharField(max_length=255,null=True,blank=True)
  created_time = models.IntegerField()
  iid = models.CharField(max_length=32) #instagram id!
  location = models.ForeignKey(InstagramLocation,null=True,blank=True)
  approved = models.BooleanField(default=getattr(settings,"APPROVE_INSTAGRAM",False))
  rejected = models.BooleanField(default=False)

  __unicode__ = lambda self: "Instagram Photo by %s"%(self.username)
  thumbnail_ = lambda self: '<img src="%s" height="75" />'%self.thumbnail.url
  thumbnail_.allow_tags=True
  @property
  def name(self):
    return "Instagram Photo by: %s"%self.username
  @property
  def datetime(self):
    return datetime.datetime.utcfromtimestamp(float(self.created_time))
  class Meta:
    ordering = ("-created_time",)
