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

kwargs = dict(widget=forms.Textarea,required=False)

from captcha.fields import ReCaptchaField

class RegistrationForm(RegistrationForm):
  captcha = ReCaptchaField()

class SurveyForm(forms.Form):
  reasons = forms.CharField(label=lr,**kwargs)
  projects = forms.CharField(label=lp,**kwargs)
  skills = forms.CharField(label=ls,help_text=s,**kwargs)
  expertise = forms.CharField(label=le,help_text=e,**kwargs)
  questions = forms.CharField(label=lq,help_text=q,**kwargs)

class UserMembershipForm(forms.ModelForm):
  class Meta:
    fields = ('by_line','bio','paypal_email','notify_global','notify_classes','notify_comments')
    model = UserMembership

class UserForm(forms.ModelForm):
  def __init__(self,*args,**kwargs):
    super(UserForm,self).__init__(*args,**kwargs)
    self.fields['first_name'].required = False
    self.fields['last_name'].required = False
    self.fields['email'].required = True
  class Meta:
    fields = ('username','first_name','last_name','email')
    model = User

class AuthenticationForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'])
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'])
        self.check_for_test_cookie()
        return self.cleaned_data
