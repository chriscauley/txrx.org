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

class Subject(Tag):
  value = lambda self: self.name
  pass

class Course(models.Model):
  name = models.CharField(max_length=64)
  subjects = models.ManyToManyField(Subject)
  description = models.TextField(null=True,blank=True,help_text=_desc_help)
  _folder = settings.UPLOAD_DIR+'/course/%Y-%m'
  src = ImageField("Logo",max_length=300,upload_to=_folder,null=True,blank=True)

  __unicode__ = lambda self: self.name

class SectionManager(models.Manager):
  def from_get(self,get):
    if not get:
      return self.all()
  live = lambda self: self.filter(starttime__gte=datetime.datetime.now())

class Section(UserModel):
  cancelled = models.BooleanField(default=False)
  full = models.BooleanField(default=False)
  course = models.ForeignKey(Course)
  location = models.ForeignKey(Location,default=1)
  fee = models.IntegerField(null=True,blank=True)
  fee_notes = models.CharField(max_length=256,null=True,blank=True)
  description = models.TextField(null=True,blank=True,help_text=_desc_help)
  starttime = models.TimeField("Time")
  date = models.DateField("First Date")
  hours = models.IntegerField(null=True,blank=True)
  sessions = models.IntegerField(null=True,blank=True)
  closed = lambda self: self.cancelled or self.full or self.starttime>datetime.datetime.now()
  _folder = settings.UPLOAD_DIR+'/course/%Y-%m'
  _h = "Will default to course logo if left blank"
  _src = ImageField("Logo",max_length=300,upload_to=_folder,null=True,blank=True,help_text=_h)
  _get_src = lambda self: self._src or self.course.src
  def _set_src(self,v): self._src = v
  src = property(_get_src,_set_src)
  tools = models.ManyToManyField(Tool,blank=True)
  objects = SectionManager()

  @property
  def first_image(self):
    fi = super(Section,self).first_image
    if fi: return fi
    return self.course.first_image

  def save(self,*args,**kwargs):
    super(Section,self).save(*args,**kwargs)
    sessions = self.session_set.order_by("starttime")
    if not sessions:
      s = Session(
        section = self,
        starttime=self.starttime,
        location=self.location,
        date=self.date
        )
      s.save()
    else: s = sessions[0]
    if self.starttime != s.starttime:
      s.startime = self.starttime
      s.save()

    # git issue #3
    # this is very hackey, user profile should be made when a user joins.
    from membership.models import Profile
    Profile.objects.get_or_create(user=self.user)
  get_description = lambda self: self.description or self.course.description
  __unicode__ = lambda self: "%s"%(self.course.name)
  class Meta:
    ordering = ("starttime",)

class Term(models.Model):
  name = models.CharField(max_length=30)
  start = models.DateField()
  end = models.DateField()
  __unicode__ = lambda self: self.name
  _s = lambda d: d.strftime("%Y%m%d")
  value = lambda self: self._s(self.start)+"|"+self._s(self.end)

class Session(Event):
  section = models.ForeignKey(Section)

class Enrollment(UserModel):
  section = models.ForeignKey(Section)
