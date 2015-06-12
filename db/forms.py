from django import forms
from django.contrib.auth import get_user_model

class StaffMemberForm(forms.ModelForm):
  def __init__(self,*args,**kwargs):
    super(StaffMemberForm,self).__init__(*args,**kwargs)
    self.fields['user'].queryset = get_user_model().objects.filter(is_staff=True)

def placeholder_fields(self):
  for field_name in self.fields:
    field = self.fields.get(field_name)
    if field and field.label:
      attrs = {'class':'form-control', 'placeholder': field.label,'title': field.label}
      if type(field.widget) in (forms.TextInput, forms.DateInput):
        field.widget = forms.TextInput(attrs=attrs)
      if type(field.widget) == (forms.PasswordInput):
        field.widget = forms.PasswordInput(attrs=attrs)
      if type(field.widget) == forms.Textarea:
        field.widget = forms.Textarea(attrs=attrs)
      if type(field.widget) == forms.EmailInput:
        field.widget = forms.EmailInput(attrs=attrs)
      """if type(field.widget) == forms.widgets.Select:
        field.empty_label = field.label
        field.label = ''"""

class PlaceholderModelForm(forms.ModelForm):
  def __init__(self,*args,**kwargs):
    super(PlaceholderModelForm, self).__init__(*args,**kwargs)
    placeholder_fields(self)

class PlaceholderForm(forms.Form):
  def __init__(self,*args,**kwargs):
    super(PlaceholderForm, self).__init__(*args,**kwargs)
    placeholder_fields(self)
