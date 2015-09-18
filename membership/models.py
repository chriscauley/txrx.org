from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import TemplateDoesNotExist
from sorl.thumbnail import ImageField

from course.models import Session, Term, Course
from lablackey.db.models import UserModel
from lablackey.utils import cached_method, cached_property
from lablackey.mail import send_template_email
from media.models import Photo
from shop.models import Product

from wmd.models import MarkDownField

import datetime, random, string, calendar

def rand32():
  seed = string.letters+string.digits
  return ''.join([random.choice(seed) for i in range(32)])

class Group(models.Model):
  name = models.CharField(max_length=64)
  order = models.IntegerField(default=0)
  __unicode__ = lambda self: self.name
  active_memberships = lambda self: self.membership_set.filter(product__isnull=False).distinct()
  class Meta:
    ordering = ("order",)

KIND_CHOICES = [
  ('bay','Bay'),
  ('drawer','Drawer')
]

class Area(models.Model):
  name = models.CharField(max_length=64)
  kind = models.CharField(max_length=64,choices=KIND_CHOICES)
  __unicode__ = lambda self: self.name
  class Meta:
    ordering = ('name',)

class Container(models.Model):
  number = models.IntegerField()
  area = models.ForeignKey(Area)
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  __unicode__ = lambda self: "%s #%s"%(self.area,self.number)
  class Meta:
    ordering = ('number',)

class Membership(models.Model):
  name = models.CharField(max_length=64)
  order = models.IntegerField("Level")
  products = cached_property(lambda self: self.product_set.filter(active=True),name="products")
  monthly_product = lambda self: self.products.filter(months=1)[0]
  yearly_product = lambda self: self.products.filter(months=12)[0]
  discount_percentage = models.IntegerField(default=0)
  group = models.ForeignKey(Group,null=True,blank=True)
  features = cached_property(lambda self:[a.feature for a in self.membershipfeature_set.all()],
                             name="features")
  @cached_property
  def all_users(self):
    return get_user_model().objects.filter(subscription__product__membership=self)
  def count_all_users(self):
    return self.all_users.count()
  def count_active_users(self):
    return self.all_users.filter(subscription__canceled__isnull=True).distinct().count()
  def profiles(self):
    return self.profile_set.all()
  class Meta:
    verbose_name = "Membership Level"
    ordering = ("order",)
  __unicode__ = lambda self: self.name

MONTHS_CHOICES = (
  (1,"Monthly"),
  (12,"Yearly"),
)

class Product(Product):
  membership = models.ForeignKey(Membership)
  months = models.IntegerField(default=1,choices=MONTHS_CHOICES)
  order = models.IntegerField(default=0)
  __unicode__ = lambda self: "%s months of %s"%(self.months,self.membership)
  def save(self,*args,**kwargs):
    self.slug = "__membershipproduct__%s"%(self.pk or random.random())
    super(Product,self).save(*args,**kwargs)
  class Meta:
    ordering = ("order",)

class Subscription(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  subscr_id = models.CharField(max_length=20,null=True,blank=True)
  created = models.DateTimeField(default=datetime.datetime.now)
  canceled = models.DateTimeField(null=True,blank=True)
  paid_until = models.DateTimeField(null=True,blank=True)
  product = models.ForeignKey(Product,null=True,blank=True)
  # self.amount should match self.product, but can be used as an override
  amount = models.DecimalField(max_digits=30, decimal_places=2, default=0)
  owed = models.DecimalField(max_digits=30, decimal_places=2, default=0)
  last_status = property(lambda self: (self.status_set.all().order_by('-datetime') or [None])[0])
  def force_canceled(self):
    self.canceled = add_months(self.last_status.datetime,self.product.months)
    self.save()
    self.recalculate()
  def bs_class(self):
    if self.owed > 0:
      return "danger"
    if self.canceled:
      return "warning"
    return "success"
  def verbose_status(self):
    if self.owed > 0:
      return "Overdue by %s"%self.owed
    if self.canceled:
      return "Canceled"
    return self.paid_until.strftime("Paid until %b %-d, %Y")
  @property
  def bg(self):
    if self.owed > 0:
      return "#ff8888"
    if self.canceled:
      return "#88ffff"
    if self.owed < 0:
      return "#88ff88"
    return "transparent"
  def recalculate(self,modify_membership=True):
    now = self.canceled or datetime.datetime.now()
    for months in range(1200): # 100 years
      if add_months(self.created,months) >= now:
        break
    amount_due = months * self.amount / self.product.months
    amount_paid = sum([s.amount for s in self.status_set.all()])
    self.owed = amount_due-amount_paid
    if self.canceled:
      self.owed = 0
    self.paid_until = add_months(self.created,int(self.product.months*amount_paid/self.amount))
    self.save()
    last = self.last_status
    if last:
      um = self.user.usermembership
      if modify_membership:
        um.membership = self.product.membership
      um.end = max(last.datetime,um.end or last.datetime)
      um.start = min(um.start or self.created,self.created)
      um.save()
    
  class Meta:
    ordering = ('created',)

PAYMENT_METHOD_CHOICES = (
  ('paypal','PayPalIPN'),
  ('cash', 'Cash'),
  ('adjustment', 'Adjustment'),
  ('refund', 'Refund'),
  ('legacy','Legacy (PayPal)'),
)

class Status(models.Model):
  amount = models.DecimalField(max_digits=30, decimal_places=2, default=0)
  subscription = models.ForeignKey(Subscription)
  paypalipn = models.ForeignKey("ipn.PayPalIPN",null=True,blank=True)
  datetime = models.DateTimeField(default=datetime.datetime.now)
  notes = models.CharField(max_length=128,null=True,blank=True)
  payment_method = models.CharField(max_length=16,choices=PAYMENT_METHOD_CHOICES,default="cash")
  def save(self,*args,**kwargs):
    super(Status,self).save(*args,**kwargs)
    self.subscription.recalculate()

  class Meta:
    ordering = ('datetime',)

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

def add_months(d,months):
  month = d.month - 1 + months
  year = d.year + month / 12
  month = month % 12 + 1
  day = min(d.day,calendar.monthrange(year,month)[1])
  return d.replace(year=year,month=month,day=day)

ORIENTATION_STATUS_CHOICES = [
  ('new','New'),
  ('emailed','Emailed'),
  ('scheduled','scheduled'),
  ('oriented','Oriented'),
]

class UserMembership(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL)
  membership = models.ForeignKey(Membership,default=1)
  start = models.DateTimeField(null=True,blank=True)
  end = models.DateTimeField(null=True,blank=True)
  voting_rights = models.BooleanField(default=False)
  suspended = models.BooleanField(default=False)
  waiver = models.FileField("Waivers",upload_to="waivers/",null=True,blank=True)
  orientation_status = models.CharField(max_length=32,choices=ORIENTATION_STATUS_CHOICES)

  photo = models.ForeignKey(Photo,null=True,blank=True)
  bio = MarkDownField(null=True,blank=True)
  api_key = models.CharField(max_length=32,default=rand32)
  _h = "A short description of what you do for the lab."
  by_line = models.CharField(max_length=50,null=True,blank=True,help_text=_h)
  name = lambda self: "%s %s"%(self.user.first_name,self.user.last_name)
  _h ="Leave blank if this is the same as your email address above."
  paypal_email = models.EmailField(null=True,blank=True,help_text=_h)
  _h = "Uncheck this to stop all email correspondance from this website "
  _h += "(same as unchecking all the below items and any future notifications we add)."
  notify_global = models.BooleanField("Global Email Preference",default=True,help_text=_h)
  _h = "If checked, you will be emailed whenever someone replies to a comment you make on this site."
  notify_comments = models.BooleanField("Comment Response Email",default=True,help_text=_h)
  _h = "If checked, you will be emailed a reminder 24 hours before a class (that you've signed up for)."
  notify_classes = models.BooleanField("Class Reminder Email",default=True,help_text=_h)
  _h = "If checked, you will be emailed new class offerings (twice a month)."
  notify_sessions = models.BooleanField("New Course Email",default=True,help_text=_h)

  __unicode__ = lambda self: "%s's Membership"%self.user
  objects = UserMembershipManager()
  @property
  def all_subscriptions(self):
    return Subscription.objects.filter(user=self.user).order_by("created")
  @cached_method
  def get_photo(self):
    return self.photo or Photo.objects.get(pk=144)
  @cached_method
  def get_term_sessions(self):
    #! Needs to be separated by something now that term is depracated!
    term = Term.objects.all()[0]
    return [(term,Session.objects.filter(user=self.user))]

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
  voters_present = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True)
  inactive_present = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name="meetings_inactive")
  nonvoters_present = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name="+")
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
  user = models.OneToOneField(settings.AUTH_USER_MODEL)
  reasons = models.TextField(blank=True)
  projects = models.TextField(blank=True)
  skills = models.TextField(blank=True)
  expertise = models.TextField(blank=True)
  questions = models.TextField(blank=True)

REASON_CHOICES = [
  ("recurring_payment_skipped", "PayPal Skipped"),
  ("recurring_payment_failed", "PayPal Failed Recurring"),
  ("recurring_payment_suspended", "PayPal Suspended"),
  ("subscr_failed", "PayPal Failed Subscription"),
  ("subscr_eot", "PayPal End of Term"),
]

EMAIL_REASONS = {
  "payment_overdue": [
    "recurring_payment_skipped",
    "recurring_payment_failed",
    "recurring_payment_suspended",
    "subscr_failed",
    "subscr_eot"
  ],
}

FLAG_STATUS_CHOICES = [
  ('new','New'),
  ('first_warning', 'Warned Once'),
  ('second_warning', 'Warned Twice'),
  ('final_warning', 'Canceled'),
]

class UserFlag(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  datetime = models.DateTimeField(auto_now_add=True)
  content_type = models.ForeignKey("contenttypes.ContentType")
  object_id = models.IntegerField()
  status = models.CharField(max_length=32,default='new',choices=FLAG_STATUS_CHOICES)
  emailed = models.DateTimeField(null=True,blank=True)
  content_object = GenericForeignKey("content_type", "object_id")
  reason = models.CharField(max_length=32,choices=REASON_CHOICES)
  __unicode__ = lambda self: "%s flagged for %s"%(self.user,self.reason)
  ACTION_CHOICES = {
    # current_status: [future_status, verbose_description, days_since_flag]
    'new': ['first_warning','Send First Warning',1],
    'first_warning': ['second_warning','Send Second Warning',7],
    'second_warning': ['final_warning','Cancel and send cancellation notice', 10],
  }
  def apply_status(self,new_status):
    context = {
      'userflag': self,
      'last_warning_date': datetime.timedelta(14)+self.datetime,
    }
    try:
      send_template_email('email/overdue/%s'%new_status,self.user.email,context=context)
    except TemplateDoesNotExist:
      print "template not found %s"%new_status
    self.status = new_status
    self.emailed = datetime.datetime.now()
    self.save()
    
from listeners import *
