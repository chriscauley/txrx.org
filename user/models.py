from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core import validators
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _

from membership.models import Level
from tool.models import UserCriterion, Criterion
from redtape.models import Signature

import datetime, os

class UserManager(BaseUserManager):
  def _create_user(self, username,  email, password, is_staff, is_superuser, **extra_fields):
    if not email:
      raise ValueError('The given email must be set')
    email = self.normalize_email(email)
    user = self.model(username=username, email=email, is_staff=is_staff, is_active=True,
                      is_superuser=is_superuser, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, username, email, password=None, **extra_fields):
    return self._create_user(username, email, password, False, False,**extra_fields)

  def create_superuser(self, username, email, password, **extra_fields):
    return self._create_user(username, email, password, True, True,**extra_fields)
  
  def get_or_none(self,*args,**kwargs):
    try:
      return self.get(*args,**kwargs)
    except (self.model.DoesNotExist, self.model.MultipleObjectsReturned):
      pass
  def get_from_anything(self,value):
    if not value:
      return
    return self.get_or_none(models.Q(username__iexact=value) |
                            models.Q(email__iexact=value) |
                            models.Q(paypal_email__iexact=value))

ORIENTATION_STATUS_CHOICES = [
  ('new','New'),
  ('emailed','Emailed'),
  ('scheduled','scheduled'),
  ('oriented','Oriented'),
]

staff_storage = FileSystemStorage(
  location=getattr(settings,"STAFF_ROOT",settings.MEDIA_ROOT),
  base_url=getattr(settings,"STAFF_URL","")
)

class User(AbstractBaseUser, PermissionsMixin):
  kwargs = dict(
    help_text=_('Required. 30 characters or fewer. Letters, digits, and ./+/-/_ only.'),
    validators=[
      validators.RegexValidator(
        r'^[\w\.+-]+$',
        _('Enter a valid username. This value may contain only letters, numbers '
          'and ./+/-/_ characters.'), 'invalid'),
    ],
    error_messages={'unique': _("A user with that username already exists."),}
  )
  username = models.CharField(_('username'), max_length=30, unique=True, **kwargs)
  email = models.EmailField(_('email address'), max_length=255, unique=True)
  first_name = models.CharField(_('first name'), max_length=30, blank=True)
  last_name = models.CharField(_('last name'), max_length=30, blank=True)
  _ht = _('Designates whether the user can log into this admin site.')
  is_staff = models.BooleanField(_('staff status'), default=False, help_text=_ht)
  is_active = models.BooleanField(_('active'), default=True)
  _ht = "Toolmasters can give any user access to any Tool Criteria."
  is_toolmaster = models.BooleanField(default=False,help_text=_ht)
  _ht = "Gatekeepers have 24/7 building access."
  is_gatekeeper = models.BooleanField(default=False,help_text=_ht)
  _ht = "Shopkeepers can mark receipts as received."
  is_shopkeeper = models.BooleanField(default=False,help_text=_ht)
  date_joined = models.DateTimeField(_('date joined'),auto_now_add=True)
  paypal_email = models.EmailField(max_length=255,null=True,blank=True) #! TODO make me unique
  _kwargs = dict(upload_to="%Y%m",max_length=200,null=True,blank=True)
  id_photo_date = models.DateTimeField(null=True,blank=True)
  headshot = models.FileField(verbose_name="Head Shot",storage=staff_storage,**_kwargs)
  objects = UserManager()

  #txrx fields
  level = models.ForeignKey(Level,default=1)
  orientation_status = models.CharField(max_length=32,choices=ORIENTATION_STATUS_CHOICES,default="new")

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email']

  rfids = property(lambda self: self.rfid_set.all().values_list('number',flat=True))

  @property
  def criterion_ids(self):
    return list(UserCriterion.active_objects.filter(user=self).values_list('criterion_id',flat=True))
  @property
  def signature_jsons(self):
    return [s.as_json for s in self.signature_set.all().order_by('-datetime')]
  @property
  def enrollment_jsons(self):
    return [e.as_json for e in self.enrollment_set.all().order_by("-session__first_date")]
  @property
  def locked_criterion_ids(self):
    ucs = list(UserCriterion.active_objects.filter(
      user=self,
      content_type__model='enrollment',
      object_id__in=self.enrollment_set.filter(completed__isnull=False).values_list("id")
    ).values_list('criterion_id',flat=True))
    ucs += list(UserCriterion.active_objects.filter(
      user=self,
      content_type__model='signature',
      object_id__in=self.signature_set.filter(completed__isnull=False).values_list("id")
    ).values_list('criterion_id',flat=True))
    return ucs
  class Meta:
    verbose_name = _('user')
    verbose_name_plural = _('users')
    ordering = ('username',)

  def get_absolute_url(self):
    return "/users/%s/" % urlquote(self.email)

  def get_full_name(self):
    full_name = '%s %s' % (self.first_name, self.last_name)
    return full_name.strip() or self.username

  def get_short_name(self):
    short_name = '%s %s' % (self.first_name, self.last_name[:1])
    return short_name.strip() or self.username

  def email_user(self, subject, message, from_email=None):
    send_mail(subject, message, from_email, [self.email])

  def send_welcome_email(self):
    from membership.utils import send_membership_email
    send_membership_email('email/new_member',self.email,context={'user': self},experimental=False)
    self.create_fake_safety()
    self.save()
  def create_fake_safety(self):
    defaults = {
      'content_object': self.subscription_set.all()[0]
    }
    criterion = Criterion.objects.get(id=settings.SAFETY_CRITERION_ID)
    uc, new = UserCriterion.active_objects.get_or_create(
      user=self,
      criterion=criterion,
      defaults=defaults
    )
  @property
  def has_safety_waiver(self):
    _ids = getattr(settings,"NONMEMBER_DOCUMENT_IDS",[])
    return len(_ids) <= Signature.objects.filter(user=self,document_id__in=_ids).count()

class RFID(models.Model):
  user = models.ForeignKey(User)
  number = models.CharField(max_length=16,unique=True)
  added = models.DateTimeField(auto_now_add=True)
  __unicode__ = lambda self: "%s (%s)"%(self.user,self.number)

class UserNote(models.Model):
  user = models.ForeignKey(User)
  note = models.CharField(max_length=256)
  added = models.DateTimeField(auto_now_add=True)

class UserCheckinManager(models.Manager):
  def checkin_today(self,*args,**kwargs):
    defaults = kwargs.pop('defaults',{})
    try:
      return self.get(time_in__gte=datetime.date.today(),*args,**kwargs), False
    except self.model.DoesNotExist:
      kwargs.update(defaults)
      return self.create(*args,**kwargs), True

class UserCheckin(models.Model):
  user = models.ForeignKey(User)
  time_in = models.DateTimeField(auto_now_add=True)
  time_out = models.DateTimeField(null=True,blank=True)
  content_type = models.ForeignKey("contenttypes.ContentType")
  object_id = models.IntegerField()
  content_object = GenericForeignKey('content_type', 'object_id')
  objects = UserCheckinManager()

from .listeners import *
