from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from membership.models import Level

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

ORIENTATION_STATUS_CHOICES = [
  ('new','New'),
  ('emailed','Emailed'),
  ('scheduled','scheduled'),
  ('oriented','Oriented'),
]

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
  email = models.EmailField(_('email address'), max_length=254, unique=True)
  first_name = models.CharField(_('first name'), max_length=30, blank=True)
  last_name = models.CharField(_('last name'), max_length=30, blank=True)
  _ht = _('Designates whether the user can log into this admin site.')
  is_staff = models.BooleanField(_('staff status'), default=False, help_text=_ht)
  is_active = models.BooleanField(_('active'), default=True)
  date_joined = models.DateTimeField(_('date joined'),auto_now_add=True)
  objects = UserManager()

  #txrx fields
  level = models.ForeignKey(Level,default=1)
  orientation_status = models.CharField(max_length=32,choices=ORIENTATION_STATUS_CHOICES,default="new")

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email']

  class Meta:
    verbose_name = _('user')
    verbose_name_plural = _('users')
    ordering = ('username',)

  def get_absolute_url(self):
    return "/users/%s/" % urlquote(self.email)

  def get_full_name(self):
    full_name = '%s %s' % (self.first_name, self.last_name[:1])
    return full_name.strip() or self.username

  def get_short_name(self):
    return self.first_name

  def email_user(self, subject, message, from_email=None):
    send_mail(subject, message, from_email, [self.email])

  def send_welcome_email(self):
    from membership.utils import send_membership_email
    send_membership_email('email/new_member',self.user.email,experimental=False)
    self.orientation_status = 'emailed'
    self.save()

from .listeners import *
