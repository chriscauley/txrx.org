from django import forms
from django.core.files import File

from lablackey.forms import RequestModelForm
from .models import Signature, Document

import json, pdb

class SignatureForm(RequestModelForm):
  is_user_form = True
  def __init__(self, request, *args, **kwargs):
    self.document = kwargs.pop('document')
    kwargs['initial'] = { 'document': self.document }
    super(SignatureForm, self).__init__(request, *args, **kwargs)
    # generate extra fields
    self.extra_fields = []
    self.rendered_content = self.document.rendered_content
    self.form_title = self.document.name
    for field in self.document.fields_json:
      self.extra_fields.append(field['name'])
      choices = field.get('choices',[('True','True')])
      if field['type'] == 'select':
        if not field['required']:
          choices = [('',[('','No Response')])] + choices
        self.fields[field['name']] = forms.ChoiceField(required=field['required'],choices=choices,
                                                       label=field['label'])
      elif field['type'] == 'checkbox':
        self.fields[field['name']] = forms.ChoiceField(required=field['required'],choices=choices,
                                                       label=field['label'],widget=forms.widgets.CheckboxInput())
      else:
        self.fields[field['name']] = forms.CharField(required=field['required'])
  def save(self,*args,**kwargs):
    commit = kwargs.pop("commit",True)
    kwargs['commit'] = False
    instance = super(SignatureForm,self).save(*args,**kwargs)
    instance.document = self.document
    instance.data = {f:self.cleaned_data.get(f,None) for f in self.extra_fields}
    if commit:
      instance.save()
    return instance
  class Meta:
    model = Signature
    exclude = ('datetime','status','status_changed','user','data','document')
