from django.forms.models import modelformset_factory
from django import forms

from .models import Room

class RoomForm(forms.ModelForm):
  class Meta:
    model = Room
    fields = ('name','geometry','in_calendar','color')

RoomFormSet = modelformset_factory(Room,RoomForm,extra=3)
