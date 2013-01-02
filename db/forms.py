from django import forms
from django.contrib.auth.models import User

class StaffMemberForm(forms.ModelForm):
  def __init__(self,*args,**kwargs):
    super(StaffMemberForm,self).__init__(*args,**kwargs)
    self.fields['user'].queryset = User.objects.filter(is_staff=True)
