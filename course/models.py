from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from lablackey.profile.models import UserModel
from sorl.thumbnail import ImageField
import datetime

from geo.models import Location

_desc_help = "Line breaks and html tags will be preserved. Use html with care!"

class Subject(models.Model):
  name = models.CharField(max_length=32)
  value = lambda self: self.name
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
  get_absolute_url = lambda self: "/classes/term/%s/%s"%(self.id,slugify(self.name))
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
  requirements = models.CharField(max_length=256,null=True,blank=True)
  prerequisites = models.CharField(max_length=256,null=True,blank=True)
  description = models.TextField(null=True,blank=True)
  location = models.ForeignKey(Location,default=1)
  src = ImageField("Logo",max_length=300,upload_to='course/%Y-%m',null=True,blank=True)
  #tools = models.ManyToManyField(Tool,blank=True)
  max_students = models.IntegerField(default=40)
  get_instructors = lambda self: set([s.user for s in self.session_set.all()])
  __unicode__ = lambda self: "%s - %s"%(self.course.name,self.term)
  class Meta:
    ordering = ("term","course")

class Session(UserModel):
  section = models.ForeignKey(Section)
  slug = models.CharField(max_length=255)
  cancelled = models.BooleanField(default=False)
  ts_help = "Only used to set dates on creation."
  time_string = models.CharField(max_length=128,help_text=ts_help,default='not implemented')
  __unicode__ = lambda self: "%s (%s - %s)"%(self.section, self.user,self.first_date.date())

  closed = property(lambda self: self.cancelled or self.archived or self.full)
  full = property(lambda self: self.enrollment_set.count() >= self.section.max_students)
  archived = property(lambda self: self.first_date<datetime.datetime.now())
  @property
  def week(self):
    sunday = self.first_date.date()-datetime.timedelta(self.first_date.weekday()+1)
    return (sunday,sunday+datetime.timedelta(6))
  subjects = property(lambda self: self.section.course.subjects.all())
  @property
  def closed_string(self):
    if self.cancelled:
      return "cancelled"
    if self.archived:
      return "closed"
    return "full"
  def save(self,*args,**kwargs):
    from membership.models import UserMembership
    profile,new = UserMembership.objects.get_or_create(user=self.user)
    if not self.id:
      self.slug = 'arst'
      super(Session,self).save(*args,**kwargs)
    self.slug = slugify("%s_%s"%(self.section,self.id))
    return super(Session,self).save(*args,**kwargs)
  def get_absolute_url(self):
    return reverse('course:detail',args=[self.slug])
  @property
  def first_date(self):
    if self.classtime_set.count():
      return self.classtime_set.all()[0].start
    return datetime.datetime(2000,1,1)
  class Meta:
    ordering = ('section',)

class ClassTime(models.Model):
  session = models.ForeignKey(Session)
  start = models.DateTimeField()
  end_time = models.TimeField()
  class Meta:
    ordering = ("start",)


class Enrollment(UserModel):
  session = models.ForeignKey(Session)

from .listeners import *
