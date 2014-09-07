from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField

from db.models import UserModel
from media.models import Photo
from course.models import Session, Term, Course
from txrx.utils import cached_method, cached_property
from project.models import Project

from wmd.models import MarkDownField
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^wmd\.models\.MarkDownField"])

import datetime, random, string

def rand32():
  seed = string.letters+string.digits
  return ''.join([random.choice(seed) for i in range(32)])

class MembershipGroup(models.Model):
  name = models.CharField(max_length=64)
  order = models.IntegerField(default=0)
  __unicode__ = lambda self: self.name
  active_memberships = lambda self: self.membership_set.filter(membershiprate__isnull=False).distinct()
  class Meta:
    ordering = ("order",)

class Membership(models.Model):
  name = models.CharField(max_length=64)
  order = models.IntegerField("Level")
  rates = cached_property(lambda self: self.membershiprate_set.all(),name="rates")
  monthly_rate = lambda self: self.rates.filter(months=1)[0]
  yearly_rate = lambda self: self.rates.filter(months=12)[0]
  discount_percentage = models.IntegerField(default=0)
  membershipgroup = models.ForeignKey(MembershipGroup,null=True,blank=True)
  features = cached_property(lambda self:[a.feature for a in self.membershipfeature_set.all()],
                             name="features")
  def profiles(self):
    return self.profile_set.all()
  class Meta:
    verbose_name = "Membership Level"
    ordering = ("order",)
  __unicode__ = lambda self: self.name

class MembershipRate(models.Model):
  membership = models.ForeignKey(Membership)
  cost = models.IntegerField()
  months = models.IntegerField(default=1)
  description = models.CharField(max_length=128)
  order = models.IntegerField(default=0)
  class Meta:
    ordering = ("order",)

class Role(models.Model):
  name = models.CharField(max_length=64)

class Feature(models.Model):
  text = models.CharField(max_length=128)
  __unicode__ = lambda self: self.text
  class Meta:
    ordering = ('text',)

class MembershipFeature(models.Model):
  feature = models.ForeignKey(Feature)
  membership = models.ForeignKey(Membership)
  order = models.IntegerField(default=0)
  class Meta:
    ordering = ("order",)

class UserMembershipManager(models.Manager):
  def list_instructors(self,**kwargs):
    from course.models import Session
    return set([s.user.usermembership for s in Session.objects.filter(**kwargs)])

class UserMembership(models.Model):
  user = models.OneToOneField(User)
  membership = models.ForeignKey(Membership,default=1)
  voting_rights = models.BooleanField(default=False)
  suspended = models.BooleanField(default=False)

  #roles = models.ManyToManyField(Role,null=True,blank=True)
  photo = models.ForeignKey(Photo,null=True,blank=True)
  bio = MarkDownField(null=True,blank=True)
  api_key = models.CharField(max_length=32,default=rand32)
  _h = "A short description of what you do for the lab."
  by_line = models.CharField(max_length=50,null=True,blank=True,help_text=_h)
  name = lambda self: "%s %s"%(self.user.first_name,self.user.last_name)
  _h ="Leave blank if this is the same as your email address above."
  paypal_email = models.EmailField(null=True,blank=True,help_text=_h)
  _h = "Uncheck this to stop all email correspondance from this website (same as unchecking all the below items and any future notifications we add)."
  notify_global = models.BooleanField("Global Email Preference",default=True,help_text=_h)
  _h = "If checked, you will be emailed whenever someone replies to a comment you make on this site."
  notify_comments = models.BooleanField("Comment Response Email",default=True,help_text=_h)
  _h = "If checked, you will be emailed a reminder 24 hours before a class (that you've signed up for)."
  notify_classes = models.BooleanField("Class Reminder Email",default=True,help_text=_h)
  _h = "If checked, you will be emailed new class offerings (twice a month)."
  notify_sessions = models.BooleanField("New Course Email",default=True,help_text=_h)

  __unicode__ = lambda self: "%s's Membership"%self.user
  objects = UserMembershipManager()
  @cached_method
  def get_photo(self):
    return self.photo or Photo.objects.get(pk=144)

  @cached_method
  def get_term_sessions(self):
    terms = Term.objects.exclude(name__icontains='test')
    out = []
    for term in terms:
      out.append((term,Session.objects.filter(user=self.user,section__term=term)))
    return [t for t in out if t[1]]
  @cached_method
  def get_projects(self):
    return Project.objects.filter(author=self.user)

class OfficerManager(models.Manager):
  def current(self,*args,**kwargs):
    kwargs['end__isnull'] = True
    return self.filter(*args,**kwargs)
  def past(self,*args,**kwargs):
    kwargs['end__isnull'] = False
    return self.filter(*args,**kwargs)

class Officer(UserModel):
  position = models.CharField(max_length=50)
  start = models.DateField(default=datetime.date.today)
  end = models.DateField(null=True,blank=True)
  order = models.IntegerField(default=999)
  objects = OfficerManager()
  __unicode__ = lambda self: "%s as %s"%(self.user,self.position)
  class Meta:
    ordering = ('order','end')

class UnsubscribeLink(UserModel):
  key = models.CharField(max_length=32,unique=True)
  created = models.DateField(auto_now_add=True)
  get_absolute_url = lambda self: "/membership/unsubscribe/%s/"%self.key

  @classmethod
  def new(clss,user):
    seed = string.letters+string.digits
    key = ''.join([random.choice(seed) for i in range(32)])
    return clss(key=key,user=user)

class LimitedAccessKey(UserModel):
  """
  Used to handle user operations that do not require login.
  A user can change email preferences and fill out evaluations with this.
  """
  key = models.CharField(max_length=32,unique=True)
  created = models.DateField(auto_now_add=True)
  expires = models.DateField()

  def save(self,*args,**kwargs):
    self.expires = datetime.datetime.now()+datetime.timedelta(7)
    return super(LimitedAccessKey,self).save(*args,**kwargs)

  @classmethod
  def new(clss,user):
    key = rand32()
    out = clss(key=key,user=user)
    out.save()
    return out

class MeetingMinutes(models.Model):
  date = models.DateField(default=datetime.date.today,unique=True)
  voters_present = models.ManyToManyField(User,null=True,blank=True)
  inactive_present = models.ManyToManyField(User,null=True,blank=True,related_name="meetings_inactive")
  nonvoters_present = models.ManyToManyField(User,null=True,blank=True,related_name="+")
  content = MarkDownField()
  _ht = "Used only when an exact list of members is unavailable (eg legacy minutes)"
  member_count = models.IntegerField(default=0,help_text=_ht)
  __unicode__ = lambda self: "Minutes: %s"%self.date
  get_absolute_url = lambda self: reverse('meeting_minutes',args=[str(self.date)])
  def get_member_count(self):
    attrs = ['voters_present','inactive_present']
    return sum([getattr(self,a).count() for a in attrs]) or self.member_count or "unknown"
  class Meta:
    ordering = ('-date',)

class Proposal(UserModel):
  order = models.IntegerField(default=0)
  title = models.CharField(max_length=256,null=True,blank=True)
  meeting_minutes = models.ForeignKey(MeetingMinutes)
  original = MarkDownField()
  ammended = MarkDownField(null=True,blank=True)
  __unicode__ = lambda self: "Proposal #%s: %s"%(self.order,self.title or "(UNNAMED)")
  final_text = property(lambda self: self.ammended or self.original)
  class Meta: 
    ordering = ('order',)

class Survey(models.Model):
  user = models.ForeignKey(User,unique=True)
  reasons = models.TextField(blank=True)
  projects = models.TextField(blank=True)
  skills = models.TextField(blank=True)
  expertise = models.TextField(blank=True)
  questions = models.TextField(blank=True)

from listeners import *
