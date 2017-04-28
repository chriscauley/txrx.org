from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.requests import RequestSite
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.conf import settings

from registration.models import RegistrationProfile

from .models import UserMembership
from .utils import verify_unique_email
from lablackey.db.forms import PlaceholderModelForm, PlaceholderForm, placeholder_fields

from registration import signals
from registration.forms import RegistrationForm

s = "What do you to hope accomplish at the hackerspace? What classes do you want to take? What classes are no offered that you'd like to see offered?"
e = "List any helpful skills or areas of expertise that might be relevent to the Lab. Also note if you would be interested in teaching classes in these areas."
q = "Please let us know about any questions or comment you may have about the lab, its procedures, or goals."

lr = "Reasons for joining %s"%settings.SITE_NAME
lp = "Previous projects of note"
ls = "Skills you desire to learn"
le = "Skills and area of expertise"
lq = "Questions or comments"

kwargs = dict(widget=forms.Textarea,required=False)

class RegistrationForm(RegistrationForm):
  first_name = forms.CharField(max_length=30,label="First Name")
  last_name = forms.CharField(max_length=30,label="Last Name")
  _ht = "If different than the email above.\n This is necessary to record when you register for a class."
  paypal_email = forms.EmailField(required=False,label="PayPal Email - Optional",help_text=_ht)
  form_title = "Create an account at %s"%settings.SITE_NAME
  def __init__(self,*args,**kwargs):
    super(RegistrationForm, self).__init__(*args,**kwargs)
    placeholder_fields(self)
  def clean_username(self,*args,**kwargs):
    username = self.cleaned_data.get("username",'')
    if "@" in username:
      raise forms.ValidationError("The @ character is not allowed in your username")
    return username
  def clean(self,*args,**kwargs):
    "Check for duplicate emails. This isn't actually used since users are sent to the password reset page before this."
    super(RegistrationForm,self).clean(*args,**kwargs)
    if not verify_unique_email(self.cleaned_data.get('email')):
      e = u'Another account is already using this email address. Please email us if you believe this is in error.'
      raise forms.ValidationError(e)
    if not verify_unique_email(self.cleaned_data.get('username')):
      e = u'Another account is already using this username. Please email us if you believe this is in error.'
      raise forms.ValidationError(e)
    return self.cleaned_data
  def save(self):
    cleaned_data = self.cleaned_data
    username, email, password = cleaned_data['username'], cleaned_data['email'], cleaned_data['password']
    if Site._meta.installed:
      site = Site.objects.get_current()
    else:
      site = RequestSite(self.request)
    new_user = RegistrationProfile.objects.create_inactive_user(username, email, password, site)
    new_user.first_name = cleaned_data['first_name']
    new_user.last_name = cleaned_data['last_name']
    new_user.save()
    signals.user_registered.send(sender=self.__class__,user=new_user,request=self.request)
    self.success_url = reverse('registration_complete')
    return new_user

class UserMembershipForm(PlaceholderModelForm):
  #! TODO: this technically is a vulnerability (someone could try to steal in very weird circumstances)
  # I need to add a verified paypal email and set it to false when they do this.
  def clean_paypal_email(self,*args,**kwargs):
    user = self.instance.user
    if not verify_unique_email(self.cleaned_data.get('paypal_email'),user=user):
      e = u'Another account is already using this paypal address. Please email us if you believe this is in error.'
      raise forms.ValidationError(e)
    return self.cleaned_data.get('paypal_email')
  class Meta:
    fields = ('by_line','bio')
    model = UserMembership

class UserForm(PlaceholderModelForm):
  def __init__(self,*args,**kwargs):
    super(UserForm,self).__init__(*args,**kwargs)
    self.fields['first_name'].required = False
    self.fields['last_name'].required = False
    self.fields['email'].required = True
  def clean_username(self,*args,**kwargs):
    username = self.cleaned_data['username']
    if not verify_unique_email(username,user=self.instance):
      e = u'Another account is already using this email address. Please email us if you believe this is in error.'
      raise forms.ValidationError(e)
    return username
  def clean_email(self,*args,**kwargs):
    email = self.cleaned_data['email']
    if not verify_unique_email(email,user=self.instance):
      e = u'Another account is already using this username. Please email us if you believe this is in error.'
      raise forms.ValidationError(e)
    return email
  class Meta:
    fields = ('username','first_name','last_name','email')
    model = get_user_model()

class AuthenticationForm(AuthenticationForm):
  def __init__(self,*args,**kwargs):
    super(AuthenticationForm, self).__init__(*args,**kwargs)
    placeholder_fields(self)
  def clean(self):
    username = self.cleaned_data.get('username')
    password = self.cleaned_data.get('password')

    if username and password:
      self.user_cache = authenticate(username=username, password=password)
      if self.user_cache is None:
        raise forms.ValidationError(
          self.error_messages['invalid_login'])
      elif not self.user_cache.is_active:
        raise forms.ValidationError(self.error_messages['inactive'])
    self.check_for_test_cookie()
    return self.cleaned_data
