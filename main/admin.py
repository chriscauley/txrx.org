from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.forms import *
from django import forms

from codrspace.admin import TaggedPhotoInline

admin.site.unregister(FlatPage)

TEMPLATE_CHOICES = (
  ('','HTML'),
  ('flatpages/markdown.html','MarkDown'),
  )

class FlatPageForm(forms.ModelForm):
  template_name = forms.CharField("Render As",help_text="",required=False)
  def __init__(self, *args, **kwargs):
    super(FlatPageForm, self).__init__(*args, **kwargs)
    self.fields['template_name'].widget = forms.Select(choices=TEMPLATE_CHOICES)
  class Meta:
    model = FlatPage

class FlatPageAdmin(FlatPageAdmin):
  form = FlatPageForm
  inlines = [TaggedPhotoInline]

admin.site.register(FlatPage,FlatPageAdmin)

from .signals import *
