from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.validators import MaxLengthValidator
from django.template.defaultfilters import slugify
from db.models import UserModel
from sorl.thumbnail import ImageField
import datetime

from feed.models import FeedItemModel
from media.models import FilesMixin, PhotosMixin
from geo.models import Location
from event.models import OccurrenceModel, reverse_ics
from tool.models import ToolsMixin
from txrx.utils import cached_method, cached_property, latin1_to_ascii

_desc_help = "Line breaks and html tags will be preserved. Use html with care!"

def to_base32(s):
  key = '-abcdefghijklmnopqrstuvwxyz'
  s = s.strip('0987654321')
  return int("0x"+"".join([hex(key.find(i))[2:].zfill(2) for i in (slugify(s)+"----")[:4]]),16)

class Subject(models.Model):
  name = models.CharField(max_length=32)
  parent = models.ForeignKey("self",null=True,blank=True)
  order = models.FloatField(default=0)
  value = lambda self: self.name
  def get_order(self):
    max_num = to_base32("zzzz")
    if self.parent:
      return to_base32(self.parent.name) + to_base32(self.name)/float(max_num)
    return to_base32(self.name)
  def save(self,*args,**kwargs):
    self.order = self.get_order()
    super(Subject,self).save(*args,**kwargs)

  def __unicode__(self):
    if self.parent:
      return "(%s) %s"%(self.parent,self.name)
    return self.name
  class Meta:
    ordering = ('order',)

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

class CourseManager(models.Manager):
  def courses_needed(self,*args,**kwargs):
    # must only look at active courses
    kwargs['active'] = kwargs.get('active',True)
    kwargs['reschedule_on__lte'] = datetime.date.today()
    query_set = self.filter(*args,**kwargs)

    # select only courses with only full and closed sessions
    courses = [course for course in query_set if not course.open_sessions]
    return courses

class Course(models.Model,PhotosMixin,ToolsMixin,FilesMixin):
  name = models.CharField(max_length=64)
  slug = lambda self: slugify(self.name)
  active = models.BooleanField(default=True) # only used with the reshedule view
  _ht = "Used for the events page."
  subjects = models.ManyToManyField(Subject)
  _folder = settings.UPLOAD_DIR+'/course/%Y-%m'
  src = ImageField("Logo",max_length=300,upload_to=_folder,null=True,blank=True)
  short_name = models.CharField(max_length=64,null=True,blank=True,help_text=_ht)
  get_short_name = lambda self: self.short_name or self.name
  __unicode__ = lambda self: self.name
  get_absolute_url = lambda self: self.sessions[0].get_absolute_url()
  sessions = lambda self: Session.objects.filter(section__course=self)
  sessions = cached_property(sessions,name="sessions")
  _ht = "The dashboard (/admin/) won't bug you to reschedule until after this date"
  reschedule_on = models.DateField(default=datetime.date.today,help_text=_ht)
  objects = CourseManager()
  def set_user_fee(self,user):
    self.user_fee = self.last_session.section.fee
    if user.is_authenticated():
      self.user_fee = self.user_fee*(100-user.usermembership.membership.discount_percentage)//100
  @cached_property
  def active_sessions(self):
    first_date = datetime.datetime.now()-datetime.timedelta(21)
    return list(self.sessions.filter(first_date__gte=first_date))
  first_date = property(lambda self: self.active_sessions[0].first_date)
  last_date = property(lambda self: self.active_sessions[-1].last_date)
  @cached_property
  def open_sessions(self):
    if self.sessions:
      return [s for s in self.sessions if not s.closed and not s.full]
  last_session = property(lambda self: (self.sessions or [None])[0])
  last_section = property(lambda self: self.last_session.section if self.last_session else None)
  def save(self,*args,**kwargs):
    super(Course,self).save(*args,**kwargs)
    #this has to be repeated in the admin because of how that works
    subjects = self.subjects.all()
    for subject in subjects:
      if subject.parent and not (subject.parent in subjects):
        self.subjects.add(subject.parent)
  class Meta:
    ordering = ("name",)

class CourseSubscription(UserModel):
  course = models.ForeignKey(Course)

class Section(models.Model,FilesMixin):
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
  _ht = "If true, this class will not raise conflict warnings for events in the same location."
  no_conflict = models.BooleanField(default=False,help_text=_ht)
  max_students = models.IntegerField(default=16)
  get_admin_url = lambda self: "/admin/course/section/%s/"%self.id

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

class Session(FeedItemModel,PhotosMixin):
  feed_item_type = 'session'
  section = models.ForeignKey(Section)
  slug = models.CharField(max_length=255)
  cancelled = models.BooleanField(default=False)
  publish_dt = models.DateTimeField(default=datetime.datetime.now) # for rss feed
  _ht = "This will be automatically updated when you save the model. Do not change"
  first_date = models.DateTimeField(default=datetime.datetime.now,help_text=_ht) # for filtering
  created = models.DateTimeField(auto_now_add=True) # for emailing new classes
  # depracated?
  ts_help = "Only used to set dates on creation."
  time_string = models.CharField(max_length=128,help_text=ts_help,default='not implemented')
  branding = models.ForeignKey(Branding,null=True,blank=True)

  __unicode__ = lambda self: latin1_to_ascii("%s (%s - %s)"%(self.section, self.user,self.first_date.date()))
  title = property(lambda self: "%s (%s)"%(self.section.course.name,self.first_date.date()))

  in_progress = property(lambda self: self.archived and self.last_date>datetime.datetime.now())
  closed = property(lambda self: self.cancelled or (self.archived and not self.in_progress))
  get_location = lambda self: self.section.location
  @cached_property
  def total_students(self):
    return sum([e.quantity for e in self.enrollment_set.all()])
  _full = lambda self: self.total_students >= self.section.max_students
  full = property(_full)
  archived = property(lambda self: self.first_date<datetime.datetime.now())
  list_users = property(lambda self: [self.user])
  description = property(lambda self: self.section.description)
  def set_user_fee(self,user):
    self.user_fee = self.section.fee
    if user.is_authenticated():
      self.user_fee = self.user_fee*(100-user.usermembership.membership.discount_percentage)//100
  @cached_property
  def first_photo(self):
    return (self.get_photos() or [super(Session,self).first_photo])[0]
  @cached_method
  def get_photos(self):
    return self._get_photos() or self.section.course.get_photos()
  # course can have files or session can override them
  @cached_method
  def get_files(self):
    return self.section.get_files() or self.section.course.get_files()

  #calendar crap
  name = property(lambda self: self.section.course.name)
  @cached_property
  def all_occurrences(self):
    # this sets self.first_date to the first ClassTime.start if they aren't equal
    # handled in the admin by /static/js/course_admin.js
    _a = self.classtime_set.all()
    if not _a[0].start == self.first_date:
      print "setting first_date"
      self.first_date = _a[0].start
      self.save()
    return _a
  get_ics_url = lambda self: reverse_ics(self)

  @cached_method
  def get_week(self):
    sunday = self.first_date.date()-datetime.timedelta(self.first_date.weekday())
    return (sunday,sunday+datetime.timedelta(6))
  
  subjects = cached_property(lambda self: self.section.course.subjects.filter(parent__isnull=True),
                             name="subjects")
  all_subjects = cached_property(lambda self: self.section.course.subjects.all(),name="all_subjects")
  @cached_property
  def related_sessions(self):
    sessions = Session.objects.filter(first_date__gte=datetime.datetime.now())
    sessions = sessions.exclude(section__course=self.section.course)
    sub_subjects = self.section.course.subjects.filter(parent__isnull=False)
    sub_sessions = list(sessions.filter(section__course__subjects__in=sub_subjects).distinct())
    if len(sub_sessions) >= 5:
      return sub_sessions
    sessions = sessions.filter(section__course__subjects__in=self.subjects.all())
    sessions = list(sessions.exclude(section__course__subjects__in=sub_subjects))
    return sub_sessions + sessions
  @property
  def closed_string(self):
    if self.cancelled:
      return "cancelled"
    if self.archived:
      return "closed"
    return "full"
  def save(self,*args,**kwargs):
    #this may be depracated, basically the site fails hard if instructors don't have membership profiles
    from membership.models import UserMembership
    profile,_ = UserMembership.objects.get_or_create(user=self.user)
    self.slug = self.slug or 'arst' # can't save without one, we'll set this below
    super(Session,self).save(*args,**kwargs)
    self.slug = slugify("%s_%s"%(self.section,self.id))
    return super(Session,self).save(*args,**kwargs)
    
  @cached_method
  def get_absolute_url(self):
    return reverse('course:detail',args=[self.slug])
  get_admin_url = lambda self: "/admin/course/session/%s/"%self.id
  get_rsvp_url = cached_method(lambda self: reverse('course:rsvp',args=[self.id]),name="get_rsvp_url")
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
    ordering = ('first_date',)

class ClassTime(OccurrenceModel):
  session = models.ForeignKey(Session)
  def short_name(self):
    times = list(self.session.classtime_set.all())
    if len(times) == 1:
      return self.session.section.course.get_short_name()
    return "%s (%s/%s)"%(self.session.section.course.get_short_name(),times.index(self)+1,len(times))
  get_absolute_url = lambda self: self.session.get_absolute_url()
  get_admin_url = lambda self: "/admin/course/session/%s/"%self.session.id
  get_location = lambda self: self.session.section.location
  no_conflict = lambda self: self.session.section.no_conflict
  description = cached_property(lambda self:self.session.section.description,name="description")
  name = cached_property(lambda self: self.session.section.course.name,name="name")
  location = cached_property(lambda self: self.session.section.location,name="location")
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

  completed = models.BooleanField(default=False)
  evaluated = models.BooleanField(default=False)
  evaluation_date = models.DateTimeField(null=True,blank=True)

  objects = EnrollmentManager()

  __unicode__ = lambda self: "%s enrolled in %s"%(self.user,self.session)
  def save(self,*args,**kwargs):
    if not self.evaluation_date:
      self.evaluation_date = list(self.session.all_occurrences)[-1].start
    super(Enrollment,self).save(*args,**kwargs)
    if self.completed:
      CourseCompletion.objects.get_or_create(user=self.user,course=self.session.section.course)
  class Meta:
    ordering = ('-datetime',)

class CourseCompletion(UserModel):
  course = models.ForeignKey(Course)
  created = models.DateTimeField(auto_now_add=True)

FIVE_CHOICES = (
  (1,'1 - Did not meet expectations'),
  (2,'2'),
  (3,'3 - Met expectations'),
  (4,'4'),
  (5,'5 - Exceeded expectations'),
)

class Evaluation(UserModel):
  _kwargs = dict(validators=[MaxLengthValidator(512)],max_length=512,null=True,blank=True)

  enrollment = models.ForeignKey(Enrollment,unique=True)
  datetime = models.DateTimeField(auto_now_add=True)

  p_ht = "Rate the instructor on subject knowledge, pace of the course and communication skills"
  presentation = models.IntegerField("Instructor Presentation",choices=FIVE_CHOICES,help_text=p_ht)
  presentation_comments = models.TextField("Comments",**_kwargs)

  c_ht = "How well did the course content cover the subject area you were interested in?"
  content = models.IntegerField("Course Content",choices=FIVE_CHOICES,help_text=c_ht)
  content_comments = models.TextField("Comments",**_kwargs)

  v_ht = "How helpful did you find the handouts and audiovisuals presented in this course?"
  visuals = models.IntegerField("Handouts/Audio/Visuals",choices=FIVE_CHOICES,help_text=v_ht)
  visuals_comments = models.TextField("Comments",**_kwargs)

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
