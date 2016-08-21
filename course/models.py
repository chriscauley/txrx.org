from django.db import models
from django.conf import settings
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse
from django.core.validators import MaxLengthValidator
from django.template.defaultfilters import slugify, truncatewords, striptags
from django.template.loader import render_to_string
from lablackey.db.models import UserModel, NamedTreeModel
from sorl.thumbnail import ImageField, get_thumbnail
from crop_override import get_override
import datetime, time

from media.models import FilesMixin, PhotosMixin
from geo.models import Room
from event.models import OccurrenceModel, reverse_ics
from tool.models import ToolsMixin, Permission, Criterion, UserCriterion, CriterionModel, Tool
from lablackey.db.models import UserModel
from lablackey.utils import cached_method, cached_property, latin1_to_ascii

from json import dumps
import os

def to_base32(s):
  key = '-abcdefghijklmnopqrstuvwxyz'
  s = s.strip('0987654321')
  return int("0x"+"".join([hex(key.find(i))[2:].zfill(2) for i in (slugify(s)+"----")[:4]]),16)

class Subject(NamedTreeModel):
  value = lambda self: self.name
  def get_order(self):
    max_num = to_base32("zzzz")
    if self.parent:
      return to_base32(self.parent.name) + to_base32(self.name)/float(max_num)
    return to_base32(self.name)
  def save(self,*args,**kwargs):
    self.order = self.get_order()
    super(Subject,self).save(*args,**kwargs)
  @property
  def as_json(self):
    return {
      'id': self.pk,
      'name': self.name,
      'children': [s.as_json for s in self.subject_set.all()],
      'value': self.pk,
      'active_courses': 0,
      'inactive_courses': 0
    }

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
    # used in admin view
    # must only look at active courses
    kwargs['active'] = kwargs.get('active',True)
    kwargs['reschedule_on__lte'] = datetime.date.today()
    query_set = self.filter(*args,**kwargs)

    # select only courses with only full and closed sessions
    courses = [course for course in query_set if not [s for s in course.active_sessions if not s.full]]
    return courses

class Course(PhotosMixin,ToolsMixin,FilesMixin,models.Model):
  name = models.CharField(max_length=64)
  slug = property(lambda self: slugify(self.name))
  active = models.BooleanField(default=True) # only used with the reshedule view
  _ht = "Used for the events page."
  short_name = models.CharField(max_length=64,null=True,blank=True,help_text=_ht)
  get_short_name = lambda self: self.short_name or self.name
  subjects = models.ManyToManyField(Subject)
  no_discount = models.BooleanField(default=False)
  @cached_property
  def first_room(self):
    return (self.courseroomtime_set.all() or [self])[0].room
  presentation = models.BooleanField("Evaluate Presentation",default=True)
  visuals = models.BooleanField("Evaluate Visuals",default=True)
  content = models.BooleanField("Evaluate Content",default=True)

  _ht = "The dashboard (/admin/) won't bug you to reschedule until after this date"
  reschedule_on = models.DateField(default=datetime.date.today,help_text=_ht)
  first_date = property(lambda self: self.active_sessions[0].first_date)
  last_date = property(lambda self: self.active_sessions[-1].last_date)
  @property
  def as_json(self):
    image = get_thumbnail(get_override(self.first_photo,'landscape_crop'),"298x199",crop="center")
    out = {
      'id': self.pk,
      'name': self.name,
      'subject_names': [s.name for s in self.subjects.all()],
      'subject_ids': [s.pk for s in self.subjects.all()],
      'url': self.get_absolute_url(),
      'im': {
        'width': image.width,
        'height': image.height,
        'url': image.url
      },
      'next_time': time.mktime(self.first_date.timetuple()) if self.active_sessions else 0,
      'fee': self.fee,
      'active_sessions': [s.as_json for s in self.active_sessions],
      'past_session_count': len(self.archived_sessions),
      'short_description': self.get_short_description(),
      'requirements': self.requirements,
      'no_discount': self.no_discount,
    }
    out['enrolled_status'] = "Enroll" if out['active_sessions'] else "Details"
    return out

  fee = models.IntegerField(null=True,blank=True,default=0)
  fee_notes = models.CharField(max_length=256,null=True,blank=True)
  requirements = models.CharField(max_length=256,null=True,blank=True)
  prerequisites = models.CharField(max_length=256,null=True,blank=True)
  description = models.TextField(null=True,blank=True)
  short_description = models.TextField(null=True,blank=True)
  get_short_description = lambda self: self.short_description or truncatewords(striptags(self.description),40)
  safety = models.BooleanField(default=False)
  room = models.ForeignKey(Room)
  def get_location_string(self):
    if self.first_room != self.room:
      s = "This class meets in the %s and then moves to the %s after a half hour lecture."
      return s%(self.first_room.name.lower(),self.room.name.lower())
    return "This class meets in the %s."%(self.room.name.lower())
  _ht = "If true, this class will not raise conflict warnings for events in the same room."
  no_conflict = models.BooleanField(default=False,help_text=_ht)
  max_students = models.IntegerField(default=16)

  objects = CourseManager()
  __unicode__ = lambda self: self.name
  get_absolute_url = lambda self: reverse("course:detail",args=[self.pk,self.slug])
  get_admin_url = lambda self: "/admin/course/course/%s/"%self.id

  @cached_method
  def get_tools(self):
    criterion_ids = Criterion.objects.filter(courses=self).values_list("id",flat=True)
    return Tool.objects.filter(permission__criteria__id__in=criterion_ids).distinct()

  @cached_property
  def active_sessions(self):
    # sessions haven't ended yet (and maybe haven't started)
    first_date = datetime.datetime.now()-datetime.timedelta(0.5)
    return list(self.sessions.filter(last_date__gte=first_date))

  @property
  def archived_sessions(self):
    # opposite of active_sessions
    first_date = datetime.datetime.now()-datetime.timedelta(0.5)
    last_year = first_date - datetime.timedelta(365)
    sessions = self.session_set.filter(last_date__lt=first_date,last_date__gte=last_year)
    return list(sessions.order_by("-first_date"))

  sessions = lambda self: Session.objects.filter(course=self,active=True)
  sessions = cached_property(sessions,name="sessions")
  last_session = lambda self: (list(self.sessions) or [None])[-1]
  def save(self,*args,**kwargs):
    super(Course,self).save(*args,**kwargs)
    #this has to be repeated in the admin because of how that works
    subjects = self.subjects.all()
    for subject in subjects:
      if subject.parent and not (subject.parent in subjects):
        self.subjects.add(subject.parent)

    reset_classes_json("Classes reset during course save")

  #! inherited from section, may not be necessary
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
    return list(set([s.user for s in self.active_sessions]))
  class Meta:
    ordering = ("name",)

DAY_CHOICES = [
  (0, "All"),
  (1, "Day 1"),
  (2, "Day 2"),
  (3, "Day 3"),
  (4, "Day 4"),
  (5, "Day 5"),
]

class SessionRoomTime(object):
  get_absolute_url = lambda self: self.session.get_absolute_url()
  get_admin_url = lambda self: self.session.get_admin_url()
  def __init__(self,**kwargs):
    for k,v in kwargs.items():
      setattr(self,k,v)
    self.end = self.start.replace(hour=self.end_time.hour,minute=self.end_time.minute)
    self.short_name = self.session.course
  def __hash__(self):
    h = hash("%s__%s__%s"%(self.short_name.id,self.start,self.end))
    print self.short_name,":","%s__%s__%s"%(self.short_name.id,self.start,self.end)
    return h

class CourseRoomTime(models.Model):
  course = models.ForeignKey(Course)
  room = models.ForeignKey(Room)
  hours_at = models.FloatField(default=0,help_text="Number of hours at location. 0 = Until class ends.")
  day = models.IntegerField(default=0,choices=DAY_CHOICES)
  order = models.IntegerField(default=999)
  __unicode__ = lambda self: "%s in %s for %s hours"%(self.get_day_display(),self.room,self.hours_at)
  seconds_at = property(lambda self: self.hours_at * 3600)
  class Meta:
    ordering = ('day','order')

class CourseSubscription(UserModel):
   course = models.ForeignKey(Course)

class Branding(models.Model):
  name = models.CharField(max_length=32)
  image = models.ImageField(upload_to="course_branding/%Y-%m")
  small_image_override = models.ImageField(upload_to="course_branding/%Y-%m",null=True,blank=True)
  get_small_image = lambda self: self.small_image_override or self.image
  __unicode__ = lambda self: self.name

class Session(UserModel,PhotosMixin,models.Model):
  def __init__(self,*args,**kwargs):
    super(Session,self).__init__(*args,**kwargs)
    if self.pk:
      # this sets self.first_date to the first ClassTime.start if they aren't equal
      # also sets self.last_date to the last ClassTime.end
      # handled in the admin by /static/js/course_admin.js
      _a = self.all_occurrences
      if not _a:
        return
      if not _a[0].start == self.first_date:
        self.first_date = _a[0].start
        self.save()
      if not _a[-1].end == self.last_date:
        self.last_date = _a[-1].end
        self.save()
  get_ics_url = lambda self: reverse_ics(self)
  course = models.ForeignKey(Course)
  cancelled = models.BooleanField(default=False)
  active = models.BooleanField(default=True)
  _ht = "Private classes cannot be signed up for and do not appear on the session page unless " \
        "the user is manually enrolled. It will appear on calendar but it will be marked in red."
  private = models.BooleanField(default=False,help_text=_ht)
  notified = models.DateTimeField(null=True,blank=True)
  publish_dt = models.DateTimeField(null=True,blank=True)
  _ht = "This will be automatically updated when you save the model. Do not change"
  first_date = models.DateTimeField(default=datetime.datetime.now,help_text=_ht) # for filtering
  last_date = models.DateTimeField(default=datetime.datetime.now,help_text=_ht) # for filtering
  created = models.DateTimeField(auto_now_add=True) # for emailing new classes
  # depracated?
  branding = models.ForeignKey(Branding,null=True,blank=True)
  needed = models.TextField("What is needed?",blank=True,default="")
  needed_completed = models.DateField(null=True,blank=True)

  __unicode__ = lambda self: latin1_to_ascii("%s (%s - %s)"%(self.course, self.user,self.first_date.date()))
  title = property(lambda self: "%s (%s)"%(self.course.name,self.first_date.date()))

  in_progress = property(lambda self: self.first_date<datetime.datetime.now()<self.last_date)
  past = property(lambda self: datetime.datetime.now() > self.last_date)
  closed = property(lambda self: self.cancelled or (self.past and not self.in_progress))
  @property
  def as_json(self):
    short_dates = self.get_short_dates()
    enrolled_status = "Enrolled: %s"%short_dates
    if datetime.datetime.now() > self.last_date:
      d = self.last_date
      enrolled_status = "Completed: %s/%s/%s"%(d.month,d.day,d.year)
    closed_status = self.closed_string if (self.closed or self.full) else None
    if self.private:
      closed_status = 'private'
    return {
      'id': self.pk,
      'name': "<b>%s</b> %s"%(self.course,short_dates),
      'course_name': self.course.name,
      'closed_status': closed_status,
      'short_dates': short_dates,
      'instructor_name': self.get_instructor_name(),
      'instructor_pk': self.user_id,
      'course_id': self.course_id,
      'enrolled_status': enrolled_status,
      'classtimes': [c.as_json for c in self.classtime_set.all()],
      'private': True,
    }
  json = property(lambda self: dumps(self.as_json))
  get_room = lambda self: self.course.room

  total_students = property(lambda self: sum([e.quantity for e in self.enrollment_set.all()]))
  evaluated_students = property(lambda self: self.get_evaluations().count())
  completed_students = property(lambda self: self.enrollment_set.filter(completed__isnull=False).count())
  full = property(lambda self: self.total_students >= self.course.max_students)
  list_users = property(lambda self: [self.user])

  #! mucch of this if deprecated after course remodel
  description = property(lambda self: self.course.description)
  @cached_property
  def first_photo(self):
    return (self.get_photos() or [super(Session,self).first_photo])[0]
  @cached_method
  def get_photos(self):
    return self._get_photos() or self.course.get_photos()

  #calendar crap
  name = property(lambda self: self.course.name)
  all_occurrences = cached_property(lambda self:list(self.classtime_set.all()),
                                    name='all_occurrences')
  get_ics_url = lambda self: reverse_ics(self)

  @cached_method
  def get_week(self):
    sunday = self.first_date.date()-datetime.timedelta(self.first_date.weekday())
    return (sunday,sunday+datetime.timedelta(6))
  
  subjects = cached_property(lambda self: self.course.subjects.filter(parent__isnull=True),
                             name="subjects")
  all_subjects = cached_property(lambda self: self.course.subjects.all(),name="all_subjects")
  @cached_property
  def related_sessions(self):
    sessions = Session.objects.filter(first_date__gte=datetime.datetime.now(),active=True)
    sessions = sessions.exclude(course=self.course)
    sub_subjects = self.course.subjects.filter(parent__isnull=False)
    sub_sessions = list(sessions.filter(course__subjects__in=sub_subjects).distinct())
    if len(sub_sessions) >= 5:
      return sub_sessions
    sessions = sessions.filter(course__subjects__in=self.subjects.all())
    sessions = list(sessions.exclude(course__subjects__in=sub_subjects))
    return sub_sessions + sessions
  @property
  def closed_string(self): #! may be depracated
    if self.cancelled:
      return "cancelled"
    if self.past:
      return "past"
    return "full"
  def save(self,*args,**kwargs):
    #this may be depracated, basically the site fails hard if instructors don't have membership profiles
    from membership.models import UserMembership
    if not self.pk and self.course:
      c = self.course
      c.active = True
      c.save()
    if self.active and not self.publish_dt:
      publish_dt = datetime.datetime.now()
    profile,_ = UserMembership.objects.get_or_create(user=self.user)
    super(Session,self).save(*args,**kwargs)

    # now a class product needs to be made (or not)
    defaults = {'slug': "%s_%s"%(unicode(self)[:40],self.pk),'name': unicode(self)}
  @cached_method
  def get_absolute_url(self):
    return self.course.get_absolute_url()
  get_admin_url = lambda self: "/admin/course/session/%s/"%self.id
  get_rsvp_url = cached_method(lambda self: reverse('course:rsvp',args=[self.id]),name="get_rsvp_url")
  def get_instructor_name(self):
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
  def get_evaluations(self):
    return Evaluation.objects.filter(enrollment__session=self)

  class Meta:
    ordering = ('first_date',)

class ClassTime(OccurrenceModel):
  session = models.ForeignKey(Session)
  emailed = models.DateTimeField(null=True,blank=True)
  def short_name(self):
    times = list(self.session.classtime_set.all())
    s = self.session.course.get_short_name()
    if len(times) != 1:
      s = "%s (%s/%s)"%(s,times.index(self)+1,len(times))
    if self.session.private:
      return "[PRIVATE] " + s
    return s
  get_absolute_url = lambda self: self.session.get_absolute_url()
  get_absolute_url = cached_method(get_absolute_url,name='get_absolute_url')
  get_admin_url = lambda self: "/admin/course/session/%s/"%self.session.id
  get_room = lambda self: self.session.course.room
  no_conflict = lambda self: self.session.course.no_conflict
  description = cached_property(lambda self:self.session.course.description,name="description")
  name = cached_property(lambda self: self.session.course.name,name="name")
  room = cached_property(lambda self: self.session.course.room,name="room")
  icon = property(lambda self: 'private' if self.session.private else 'course')
  @property
  def as_json(self):
    room = self.session.course.first_room
    return {
      'room_id': self.session.course.room_id,
      'session_id': self.session_id,
      'name': self.short_name(),
      'start': str(self.start),
      'end': str(self.end),
      #! this should just be an id on session or course with a separate lookup
      'first_room': { 'id': room.id, 'name': room.name }
    }
  @cached_method
  def build_class_times(self):
    course = self.session.course

    # 1-indexed day number
    daynumber = self.session.classtime_set.filter(start__gte=self.start).count()
    roomtimes = course.courseroomtime_set.filter(day=daynumber)
    roomtimes = roomtimes or course.courseroomtime_set.filter(day=0)
    if not roomtimes:
      return [self]
    out = []
    current_datetime = self.start
    for roomtime in roomtimes:
      remaining = self.end-current_datetime
      occurrence = SessionRoomTime(
        start=current_datetime,
        end_time=(current_datetime + datetime.timedelta(0,roomtime.seconds_at) or remaining).time(),
        name = "%s at %s for %s hours"%(course,roomtime.room,roomtime.hours_at),
        room = roomtime.room,
        session = self.session
      )
      current_datetime = occurrence.end
      out.append(occurrence)
    if occurrence.end != self.end:
      remaining = current_datetime-self.end
      occurrence = SessionRoomTime(
        start=current_datetime,
        end_time=self.end_time,
        room = roomtime.room,
        name = "%s at %s until end (%s)"%(course,course.room,occurrence.end_time),
        session = self.session,
      )
      out.append(occurrence)
    return out
  class Meta:
    ordering = ("start",)

class EnrollmentManager(models.Manager):
  def pending_evaluation(self,*args,**kwargs):
    kwargs['evaluation_date__lte'] = datetime.datetime.now()
    kwargs['evaluation_date__gte'] = datetime.datetime.now()-datetime.timedelta(60)
    kwargs['evaluated'] = False
    kwargs['emailed'] = False
    return self.filter(*args,**kwargs)

class Enrollment(CriterionModel):
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  session = models.ForeignKey(Session)
  quantity = models.IntegerField(default=1)

  evaluated = models.BooleanField(default=False)
  emailed = models.BooleanField(default=False)
  evaluation_date = models.DateTimeField(null=True,blank=True)
  transaction_ids = models.TextField(null=True,blank=True)
  get_occurrences = lambda self: list(session.classtime_set.all())

  objects = EnrollmentManager()

  get_criteria = lambda self: self.session.course.criterion_set.all()
  @property
  def as_json(self):
    return {
      'id': self.id,
      'session': self.session.as_json,
      'session_name': unicode(self.session),
      'completed': unicode(self.completed or ''),
    }

  __unicode__ = lambda self: "%s enrolled in %s"%(self.user,self.session)
  def save(self,*args,**kwargs):
    if not self.evaluation_date:
      self.evaluation_date = list(self.session.all_occurrences)[-1].start
    super(Enrollment,self).save(*args,**kwargs)
  class Meta:
    ordering = ('-datetime',)

FIVE_CHOICES = (
  (1,'1 - Did not meet expectations'),
  (2,'2'),
  (3,'3 - Met expectations'),
  (4,'4'),
  (5,'5 - Exceeded expectations'),
)

class Evaluation(UserModel):
  _kwargs = dict(validators=[MaxLengthValidator(512)],max_length=512,null=True,blank=True)

  enrollment = models.OneToOneField(Enrollment)
  datetime = models.DateTimeField(auto_now_add=True)

  p_ht = "Rate the instructor on subject knowledge, pace of the course and communication skills"
  presentation = models.IntegerField("Instructor Presentation",choices=FIVE_CHOICES,help_text=p_ht,default=0)
  presentation_comments = models.TextField("Comments",**_kwargs)

  c_ht = "How well did the course content cover the subject area you were interested in?"
  content = models.IntegerField("Course Content",choices=FIVE_CHOICES,help_text=c_ht,default=0)
  content_comments = models.TextField("Comments",**_kwargs)

  v_ht = "How helpful did you find the handouts and audio visuals presented in this course?"
  visuals = models.IntegerField("Handouts/Audio/Visuals",choices=FIVE_CHOICES,help_text=v_ht,default=0)
  visuals_comments = models.TextField("Comments",**_kwargs)

  question1 = models.TextField("What did you like best about this class?",null=True,blank=True)
  question2 = models.TextField("How could this class be improved?",null=True,blank=True)
  question3 = models.TextField("What motivated you to take this class?",null=True,blank=True)
  question4 = models.TextField("What classes would you like to see offered in the future?",null=True,blank=True)

  _ht = "If checked your evaluation will be anonymous. If so the staff will not be able to respond to any questions you may have."
  anonymous = models.BooleanField("Evaluate Anonymously",default=False,help_text=_ht)
  def get_user(self):
    return "Anonymous" if self.anonymous else str(self.user.email)

  __unicode__ = lambda self: "%s Evaluation for %s"%(self.get_user(),self.enrollment.session)
  number_fields = ["presentation","content","visuals"]
  def get_number_tuples(self):
    return [(f,getattr(self,f),getattr(self,f+"_comments")) for f in self.number_fields]
  question_fields = property(lambda self: ['question'+str(i) for i in range(1,5)])
  def get_question_tuples(self):
    _t = [(s.title()+" comments",getattr(self,s+'_comments')) for s in self.number_fields]
    _t += [(self._meta.get_field(q).verbose_name,getattr(self,q)) for q in self.question_fields]
    return [t for t in _t if t[1]] #filter out unanswered quesions

  def save(self,*args,**kwargs):
    super(Evaluation,self).save(*args,**kwargs)
    e = self.enrollment
    e.evaluated = True
    e.save()

  class Meta:
    ordering = ('-datetime',)

def reset_classes_json(context="no context provided"):
  values = {
    'courses': dumps([c.as_json for c in Course.objects.filter(active=True)]),
    'subjects': dumps([s.as_json for s in Subject.objects.filter(parent=None)]),
  }
  text = render_to_string('course/classes.json',values)
  f = open(os.path.join(settings.STATIC_ROOT,'_classes.json'),'w')
  f.write(text)
  f.close()
  os.rename(os.path.join(settings.STATIC_ROOT,'_classes.json'),os.path.join(settings.STATIC_ROOT,'classes.json'))

  cutoff = datetime.datetime.now() - datetime.timedelta(1)
  text = dumps([s.pk for s in Session.objects.filter(last_date__gte=cutoff) if s.full or s.private])
  f = open(os.path.join(settings.STATIC_ROOT,'_sessions.json'),'w')
  f.write("var FULL_SESSIONS = "+text)
  f.close()
  os.rename(os.path.join(settings.STATIC_ROOT,'_sessions.json'),os.path.join(settings.STATIC_ROOT,'sessions.json'))

  # for now email chris whenever this happens so that he can check
  # if it's firing too often or during a request
  dt = datetime.datetime.now()
  if dt.hour == 0 and dt.minute == 0:
    mail_admins("classes.json reset",context)

from .listeners import *
