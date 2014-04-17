from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import UserMembership

from registration.forms import RegistrationForm

s = "What do you to hope accomplish at the hackerspace? What classes do you want to take? What classes are no offered that you'd like to see offered?"
e = "List any helpful skills or areas of expertise that might be relevent to the Lab. Also note if you would be interested in teaching classes in these areas."
q = "Please let us know about any questions or comment you may have about the lab, its procedures, or goals."

lr = "Reasons for joining TX/RX Labs"
lp = "Previous projects of note"
ls = "Skills you desire to learn"
le = "Skills and area of expertise"
lq = "Questions or comments"

def verify_unique_email(email,user=None):
  """
  Check to make sure that there are no other users with this email.
  Can be used with email or username.
  """
  other_users = User.objects.all()
  if user:
    other_users = User.objects.exclude(pk=user.pk)
  by_email = other_users.filter(email=email)
  by_username = other_users.filter(username=email)
  by_paypal_email = other_users.filter(usermembership__paypal_email=email)
  return not (by_email or by_username or by_paypal_email)

kwargs = dict(widget=forms.Textarea,required=False)

from captcha.fields import ReCaptchaField

class RegistrationForm(RegistrationForm):
  captcha = ReCaptchaField()
  def clean(self,*args,**kwargs):
    "Check for duplicate emails. This isn't actually used since users are sent to the password reset page before this."
    super(RegistrationForm,self).clean(*args,**kwargs)
    user = self.instance
    if not verify_unique_email(self.cleaned_data.get('email'),user=user):
      e = u'Another account is already using this email address. Please email us if you believe this is in error.'
      raise forms.ValidationError(e)
    if not verify_unique_email(self.cleaned_data.get('username'),user=user):
      e = u'Another account is already using this username. Please email us if you believe this is in error.'
      raise forms.ValidationError(e)
    return email

class SurveyForm(forms.Form):
  reasons = forms.CharField(label=lr,**kwargs)
  projects = forms.CharField(label=lp,**kwargs)
  skills = forms.CharField(label=ls,help_text=s,**kwargs)
  expertise = forms.CharField(label=le,help_text=e,**kwargs)
  questions = forms.CharField(label=lq,help_text=q,**kwargs)

class UserMembershipForm(forms.ModelForm):
  def clean_paypal_email(self,*args,**kwargs):
    user = self.instance
    if not verify_unique_email(self.cleaned_data.get('paypal_email'),user=user):
      e = u'Another account is already using this paypal address. Please email us if you believe this is in error.'
      raise forms.ValidationError(e)
    return self.cleaned_data.get('paypal_email')
  class Meta:
    fields = ('by_line','bio','paypal_email','notify_global','notify_classes','notify_comments','notify_sessions')
    model = UserMembership

class UserForm(forms.ModelForm):
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
    model = User

class AuthenticationForm(AuthenticationForm):
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
