from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.sites.requests import RequestSite
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.conf import settings

from .models import UserMembership
from .utils import verify_unique_email
from lablackey.forms import RequestModelForm
from lablackey.db.forms import PlaceholderModelForm, PlaceholderForm, placeholder_fields

from lablackey.registration import signals
from lablackey.registration.models import RegistrationProfile

import random

s = "What do you to hope accomplish at the hackerspace? What classes do you want to take? What classes are no offered that you'd like to see offered?"
e = "List any helpful skills or areas of expertise that might be relevent to the Lab. Also note if you would be interested in teaching classes in these areas."
q = "Please let us know about any questions or comment you may have about the lab, its procedures, or goals."

lr = "Reasons for joining %s"%settings.SITE_NAME
lp = "Previous projects of note"
ls = "Skills you desire to learn"
le = "Skills and area of expertise"
lq = "Questions or comments"

kwargs = dict(widget=forms.Textarea,required=False)

class SignUpForm(RequestModelForm):
  reset_link = '<a href="/auth/password_reset/">reset your password</a>'
  email = forms.EmailField(max_length=200,error_messages={
    'unique': 'An account with this email already exists.<br /> Enter another or {}.'.format(reset_link)
  })
  _ht = "If different than the email above.\n This is necessary to record when you register for a class."
  paypal_email = forms.EmailField(required=False,label="PayPal Email - Optional",help_text=_ht)
  #! TODO this is currently set in the auth modal
  # form_title = "Create an account at %s"%settings.SITE_NAME
  password = forms.CharField(label="Password",strip=False,widget=forms.PasswordInput)
  html_errors = ["non_field_error","email","paypal_email"]
  @classmethod
  def user_is_allowed(clss,request):
    if request.user.is_authenticated():
      raise NotImplementedError()
    return True
  @classmethod
  def get_page_json(clss,page=0):
    return dict(
      page=page,
      results=[],
    )
  def clean_password(self,*args,**kwargs):
    password = self.cleaned_data.get("password",'')
    if len(password) < 8:
      raise forms.ValidationError("Password must be at least 8 characters.")
    return password
  def clean_paypal_email(self,*args,**kwargs):
    paypal_email = self.cleaned_data.get("paypal_email",'')
    if not verify_unique_email(self.cleaned_data.get('paypal_email')):
      e = "An account with this paypal_email already exists.<br/> Enter another or {}.".format(self.reset_link)
      raise forms.ValidationError(e)
    return paypal_email
  def clean(self,*args,**kwargs):
    "Check for duplicate emails. This isn't actually used since users are sent to the password reset page before this."
    super(SignUpForm,self).clean(*args,**kwargs)
    if not verify_unique_email(self.cleaned_data.get('email')):
      e = u'Another account is already using this email address. <br/ >'
      e+= u'Enter another or <a href="/auth/password_reset/">reset your password</a>.'
      raise forms.ValidationError(e)
    return self.cleaned_data
  def save(self):
    cleaned_data = self.cleaned_data
    email, password = cleaned_data['email'], cleaned_data['password']
    username = email.split("@")[0]
    extra = ""
    while get_user_model().objects.filter(username=username+extra):
      extra = str(random.randint(1000,10000))
    username = username + extra
    site = Site.objects.get_current() if Site._meta.installed else RequestSite(self.request)
    new_user = get_user_model().objects.create_user(
      username,
      email,
      password,
      first_name=cleaned_data['first_name'],
      last_name=cleaned_data['last_name'],
    )
    new_user.paypal_email = cleaned_data.get("paypal_email",None)
    new_user.save()
    signals.user_registered.send(sender=self.__class__,user=new_user,request=self.request)
    new_user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(self.request,new_user)
    messages.success(self.request,"You are now registered and have been logged in.")
    return new_user
  class Meta:
    model = get_user_model()
    fields = ("email","password","first_name","last_name","paypal_email")

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
  @classmethod
  def user_is_allowed(clss,request):
    return True
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
  @classmethod
  def user_is_allowed(clss,request):
    return True
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
