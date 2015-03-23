from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms

from .models import Thing, Material

class ThingForm(forms.ModelForm):
  widget = FilteredSelectMultiple("Person", False, attrs={'rows':'2'})
  materials = forms.ModelMultipleChoiceField(Material.objects.all(), widget=widget)
  class Meta:
    model = Thing
    fields = ('title','description','parent_link','materials')
