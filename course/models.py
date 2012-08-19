from django.db import models
from django.conf import settings
from lablackey.profile.models import UserModel
from sorl.thumbnail import ImageField
import datetime

from lablackey.geo.models import Location
from lablackey.event.models import Event
from articles.models import Tag
from tool.models import Tool

_desc_help = "Line breaks and html tags will be preserved. Use html with care!"

class Subject(models.Model):
  name = models.CharField(max_length=32)
  __unicode__ = lambda self: self.name
  class Meta:
    ordering = ('name',)

class Term(models.Model):
  name = models.CharField(max_length=32)
  start = models.DateField()
  end = models.DateField()
  __unicode__ = lambda self: self.name
  _s = lambda d: d.strftime("%Y%m%d")
  value = lambda self: self._s(self.start)+"|"+self._s(self.end)
  class Meta:
    ordering = ('-start',)

class Course(models.Model):
  name = models.CharField(max_length=64)
  subjects = models.ManyToManyField(Subject)
  _folder = settings.UPLOAD_DIR+'/course/%Y-%m'
  src = ImageField("Logo",max_length=300,upload_to=_folder,null=True,blank=True)
  __unicode__ = lambda self: self.name
  class Meta:
    ordering = ("name",)

class Section(models.Model):
  course = models.ForeignKey(Course)
  term = models.ForeignKey("Term")
  fee = models.IntegerField(null=True,blank=True)
  fee_notes = models.CharField(max_length=256,null=True,blank=True)
  description = models.TextField(null=True,blank=True)
  location = models.ForeignKey(Location,default=1)
  src = ImageField("Logo",max_length=300,upload_to='course/%Y-%m',null=True,blank=True)
  tools = models.ManyToManyField(Tool,blank=True)
  cancelled = models.BooleanField(default=False)
  max_students = models.IntegerField(default=40)
  closed = lambda self: self.cancelled or self.starttime>datetime.datetime.now()

  get_instructors = lambda self: set([s.user for s in self.session_set.all()])
      
  __unicode__ = lambda self: "%s - %s"%(self.course.name,self.term)
  class Meta:
    ordering = ("term","course")

class Session(UserModel):
  section = models.ForeignKey(Section)
  ts_help = "Only used to set dates on creation."
  time_string = models.CharField(max_length=128,help_text=ts_help,default='not implimented')
  __unicode__ = lambda self: "%s (%s)"%(self.section, self.user)

class ClassTime(models.Model):
  session = models.ForeignKey(Session)
  start = models.DateTimeField()
  end_time = models.TimeField()
  class Meta:
    ordering = ("start",)


class Enrollment(UserModel):
  session = models.ForeignKey(Session)
