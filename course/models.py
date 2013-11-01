from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from db.models import UserModel
from sorl.thumbnail import ImageField
import datetime

from codrspace.models import SetModel, MiscFile
from geo.models import Location
from event.models import OccurrenceModel, reverse_ics
from txrx.utils import cached_method,cached_property

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

class Branding(models.Model):
  name = models.CharField(max_length=32)
  image = models.ImageField(upload_to="course_branding/%Y-%m")
  small_image_override = models.ImageField(upload_to="course_branding/%Y-%m",null=True,blank=True)
  get_small_image = lambda self: self.small_image_override or self.image
  __unicode__ = lambda self: self.name

class Session(UserModel,SetModel):
  section = models.ForeignKey(Section)
  slug = models.CharField(max_length=255)
  cancelled = models.BooleanField(default=False)
  publish_dt = models.DateTimeField(default=datetime.datetime.now) # for rss feed
  ts_help = "Only used to set dates on creation."
  time_string = models.CharField(max_length=128,help_text=ts_help,default='not implemented')
  branding = models.ForeignKey(Branding,null=True,blank=True)

  __unicode__ = lambda self: "%s (%s - %s)"%(self.section, self.user,self.first_date.date())

  in_progress = property(lambda self: self.archived and self.last_date>datetime.datetime.now())
  closed = property(lambda self: self.cancelled or (self.archived and not self.in_progress))
  full = lambda self: sum([e.quantity for e in self.enrollment_set.all()]) >= self.section.max_students
  full = property(full)
  archived = property(lambda self: self.first_date<datetime.datetime.now())
  list_users = property(lambda self: [self.user])
  description = property(lambda self: self.section.description)

  #calendar crap
  name = property(lambda self: self.section.course.name)
  all_occurrences = cached_property(lambda self: self.classtime_set.all(),name='all_occurrences')
  get_ics_url = lambda self: reverse_ics(self)

  @cached_method
  def get_week(self):
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
  @cached_property
  def first_date(self):
    if self.all_occurrences:
      return self.all_occurrences[0].start
    return datetime.datetime(2000,1,1)
  @cached_property
  def last_date(self):
    if self.all_occurrences:
      return list(self.all_occurrences)[-1].end
    return datetime.datetime(2000,1,1)
  def get_instructor_name(self):
    instructor = self.user
    if self.user.first_name and self.user.last_name:
      return "%s %s."%(self.user.first_name, self.user.last_name[0])
    return self.user.username
  def get_short_dates(self):
    dates = [ct.start for ct in self.all_occurrences]
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

class SessionAttachment(models.Model):
  session = models.ForeignKey(Session)
  attachment = models.ForeignKey(MiscFile)
  order = models.IntegerField(default=0)
  class Meta:
    ordering = ('order',)

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

class EnrollmentManager(models.Manager):
  def pending_evaluation(self,*args,**kwargs):
    kwargs['evaluation_date__lte'] = datetime.datetime.now()
    kwargs['evaluation_date__gte'] = datetime.datetime.now()-datetime.timedelta(30)
    kwargs['evaluated'] = False
    return self.filter(*args,**kwargs)

class Enrollment(UserModel):
  session = models.ForeignKey(Session)
  datetime = models.DateTimeField(default=datetime.datetime.now)
  quantity = models.IntegerField(default=1)
  evaluated = models.BooleanField(default=False)
  evaluation_date = models.DateTimeField(null=True,blank=True)
  objects = EnrollmentManager()
  __unicode__ = lambda self: "%s enrolled in %s"%(self.user,self.session)
  def save(self,*args,**kwargs):
    if not self.evaluation_date:
      self.evaluation_date = list(self.session.all_occurrences)[-1].start
    super(Enrollment,self).save(*args,**kwargs)
  class Meta:
    ordering = ('-datetime',)

FIVE_CHOICES = (
  (1,'1'),
  (2,'2'),
  (3,'3'),
  (4,'4'),
  (5,'5'),
)

class Evaluation(UserModel):
  enrollment = models.ForeignKey(Enrollment,unique=True)
  datetime = models.DateTimeField(auto_now_add=True)

  p_ht = "Rate the instructor on subject knowledge, pace of the course and communication skills"
  presentation = models.IntegerField("Instructor Presentation",choices=FIVE_CHOICES,help_text=p_ht)
  presentation_comments = models.CharField("Comments",max_length=128,null=True,blank=True)

  c_ht = "How well did the course content cover the subject area you were interested in?"
  content = models.IntegerField("Course Content",choices=FIVE_CHOICES,help_text=c_ht)
  content_comments = models.CharField("Comments",max_length=128,null=True,blank=True)

  v_ht = "How helpful did you find the handouts and audiovisuals presented in this course?"
  visuals = models.IntegerField("Handouts/Audio/Visuals",choices=FIVE_CHOICES,help_text=v_ht)
  visuals_comments = models.CharField("Comments",max_length=128,null=True,blank=True)

  question1 = models.TextField("What did you like best about this class?",null=True,blank=True)
  question2 = models.TextField("How could this class be improved?",null=True,blank=True)
  question3 = models.TextField("What motivated you to take this class?",null=True,blank=True)
  question4 = models.TextField("What classes would you like to see offered in the future?",null=True,blank=True)

  __unicode__ = lambda self: "%s evaluation for %s"%(self.user,self.enrollment.session)
  number_fields = ["presentation","content","visuals"]
  def get_number_tuples(self):
    return [(f,getattr(self,f),getattr(self,f+"_comments")) for f in self.number_fields]
  question_fields = property(lambda self: ['question'+str(i) for i in range(1,5)])
  def get_question_tuples(self):
    _t = [(self._meta.get_field(q).verbose_name,getattr(self,q)) for q in self.question_fields]
    return [t for t in _t if t[1]] #filter out unanswered quesions

  def save(self,*args,**kwargs):
    super(Evaluation,self).save(*args,**kwargs)
    e = self.enrollment
    e.evaluated = True
    e.save()

  class Meta:
    ordering = ('-datetime',)
  

from .listeners import *
