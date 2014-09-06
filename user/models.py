from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
  pass

class User(AbstractBaseUser, PermissionsMixin):
  kwargs = dict(
    help_text=_('Required. 30 characters or fewer. Letters, digits, and @/./+/-/_ only.'),
    validators=[
      validators.RegexValidator(
        r'^[\w.@+-]+$',
        _('Enter a valid username. This value may contain only letters, numbers '
          'and @/./+/-/_ characters.'), 'invalid'),
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
  date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

  objects = UserManager()

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email']

  class Meta:
    verbose_name = _('user')
    verbose_name_plural = _('users')

  def get_absolute_url(self):
    return "/users/%s/" % urlquote(self.email)

  def get_full_name(self):
    full_name = '%s %s' % (self.first_name, self.last_name)
    return full_name.strip()

  def get_short_name(self):
    return self.first_name

  def email_user(self, subject, message, from_email=None):
    send_mail(subject, message, from_email, [self.email])
