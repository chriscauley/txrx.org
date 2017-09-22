from django import forms

from notify.models import NotifySettings, METHOD_CHOICES

from lablackey.forms import RequestModelForm
from lablackey.sms.models import SMSNumber

class NotificationSettingsForm(RequestModelForm):
  new_comments = forms.ChoiceField(choices=METHOD_CHOICES,widget=forms.widgets.RadioSelect)
  my_classes = forms.ChoiceField(choices=METHOD_CHOICES,widget=forms.widgets.RadioSelect)
  new_sessions = forms.ChoiceField(choices=METHOD_CHOICES,widget=forms.widgets.RadioSelect)
  @classmethod
  def user_is_allowed(clss,self):
    return True
  def clean(self):
    try:
      has_number = self.request.user.smsnumber.verified
    except SMSNumber.DoesNotExist:
      has_number = None
    for key,value in self.cleaned_data.items():
      if value == "sms" and not has_number:
        raise forms.ValidationError({key: "You must have a validated phone number to be notified by SMS"})
  @classmethod
  def get_instance(clss,request,id=None): # id is not used
    if request.user.is_authenticated():
      return clss.Meta.model.objects.get_or_create(user=request.user)[0]
  class Meta:
    model = NotifySettings
    fields = (
      "new_comments","my_classes","new_sessions",
    )
