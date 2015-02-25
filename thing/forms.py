from django import forms

from .models import Thing

class ThingForm(forms.ModelForm):
  class Meta:
    model = Thing
    fields = ('title','description','parent_link','materials')
