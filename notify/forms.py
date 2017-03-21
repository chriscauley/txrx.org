from django import forms

from notify.models import NotifySettings, METHOD_CHOICES

class NotificationSettingsForm(forms.ModelForm):
  new_comments = forms.ChoiceField(choices=METHOD_CHOICES,widget=forms.widgets.RadioSelect)
  my_classes = forms.ChoiceField(choices=METHOD_CHOICES,widget=forms.widgets.RadioSelect)
  new_sessions = forms.ChoiceField(choices=METHOD_CHOICES,widget=forms.widgets.RadioSelect)
  @classmethod
  def get_instance(clss,request):
    return clss.Meta.model.objects.get_or_create(user=request.user)[0]
  class Meta:
    model = NotifySettings
    fields = (
      "new_comments","my_classes","new_sessions",
    )