from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from db.models import UserModel
from sorl.thumbnail import ImageField
import datetime

from codrspace.models import SetModel
from geo.models import Location
from event.models import OccurrenceModel, reverse_ics

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
  _ht = "Used for the events page."
  subjects = models.ManyToManyField(Subject)
  _folder = settings.UPLOAD_DIR+'/course/%Y-%m'
  src = ImageField("Logo",max_length=300,upload_to=_folder,null=True,blank=True)
  short_name = models.CharField(max_length=64,null=True,blank=True,help_text=_ht)
  get_short_name = lambda self: self.short_name or self.name
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
  safety = models.BooleanField(default=False)
  location = models.ForeignKey(Location,default=1)
  src = ImageField("Logo",max_length=300,upload_to='course/%Y-%m',null=True,blank=True)
  #tools = models.ManyToManyField(Tool,blank=True)
  max_students = models.IntegerField(default=40)

  __unicode__ = lambda self: "%s - %s"%(self.course.name,self.term)

  def get_notes(self):
    notes = []
    if self.requirements:
      notes.append(('Requirements',self.requirements))
    if self.fee_notes:
      notes.append(('Fee Notes',self.fee_notes))
    if self.safety:
      notes.append(('Safety',"This class has a 20 minute safety session before the first session."))
    if self.prerequisites:
      notes.append(('Prerequisites',self.prerequisites))
    return notes
  @property
  def list_users(self):
    return list(set([s.user for s in self.session_set.all()]))
  class Meta:
    ordering = ("term","course")

class Session(UserModel,SetModel):
  section = models.ForeignKey(Section)
  slug = models.CharField(max_length=255)
  cancelled = models.BooleanField(default=False)
  ts_help = "Only used to set dates on creation."
  time_string = models.CharField(max_length=128,help_text=ts_help,default='not implemented')
  __unicode__ = lambda self: "%s (%s - %s)"%(self.section, self.user,self.first_date.date())

  in_progress = property(lambda self: self.archived and self.last_date>datetime.datetime.now())
  closed = property(lambda self: self.cancelled or (self.archived and not self.in_progress) or self.full)
  full = property(lambda self: self.enrollment_set.count() >= self.section.max_students)
  archived = property(lambda self: self.first_date<datetime.datetime.now())
  list_users = property(lambda self: [self.user])

  #calendar crap
  name = property(lambda self: self.section.course.name)
  all_occurrences = property(lambda self: self.classtime_set.all())
  get_ics_url = lambda self: reverse_ics(self)

  @property
  def week(self):
    sunday = self.first_date.date()-datetime.timedelta(self.first_date.weekday())
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
  @property
  def last_date(self):
    if self.classtime_set.count():
      return list(self.classtime_set.all())[-1].end
    return datetime.datetime(2000,1,1)
  def get_instructor_name(self):
    instructor = self.user
    if self.user.first_name and self.user.last_name:
      return "%s %s."%(self.user.first_name, self.user.last_name[0])
    return self.user.username
  def get_short_dates(self):
    dates = [ct.start for ct in self.classtime_set.all()]
    month = None
    out = []
    for d in dates:
      if month != d.month:
        month = d.month
        out.append(d.strftime("%b %e"))
      else:
        out.append(d.strftime("%e"))
    return ', '.join(out)
    
  class Meta:
    ordering = ('section',)

class ClassTime(OccurrenceModel):
  session = models.ForeignKey(Session)
  start = models.DateTimeField()
  end_time = models.TimeField()
  def short_name(self):
    times = list(self.session.classtime_set.all())
    if len(times) == 1:
      return self.session.section.course.get_short_name()
    return "%s (%s/%s)"%(self.session.section.course.get_short_name(),times.index(self)+1,len(times))
  get_absolute_url = lambda self: self.session.get_absolute_url()
  get_location = lambda self: self.session.section.location
  @property
  def description(self):
    return self.session.section.description
  @property
  def name(self):
    return self.session.section.course.name
  @property
  def end(self):
    return self.start.replace(hour=self.end_time.hour,minute=self.end_time.minute)
  class Meta:
    ordering = ("start",)

class Enrollment(UserModel):
  session = models.ForeignKey(Session)
  datetime = models.DateTimeField(default=datetime.datetime.now)
  __unicode__ = lambda self: "%s enrolled in %s"%(self.user,self.session)
  class Meta:
    ordering = ('-datetime','-id')

from .listeners import *
