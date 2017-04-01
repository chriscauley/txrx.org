from django import forms
from django.core.files import File

from .models import Signature, Document

import json

class SignatureForm(forms.ModelForm):
  document = forms.ModelChoiceField(Document.objects.all(),widget=forms.HiddenInput())
  def __init__(self, *args, **kwargs):
    self.document = kwargs.pop('document')
    super(SignatureForm, self).__init__(*args, **kwargs)
    self.fields.pop('document')
    # generate extra fields
    self.extra_fields = []
    for field in self.document.fields_json:
      if field['type'] == 'header':
        continue
      self.extra_fields.append(field['name'])
      if field['type'] == 'select':
        choices = field['choices']
        if not field['required']:
          choices = [('',[('','No Response')])] + choices
        self.fields[field['name']] = forms.ChoiceField(required=field['required'],choices=choices,
                                                        label=field['label'])
      else:
        self.fields[field['name']] = forms.CharField(required=field['required'])
      
  def save(self,*args,**kwargs):
    commit = kwargs.pop("commit",True)
    kwargs['commit'] = False
    instance = super(SignatureForm,self).save(*args,**kwargs)
    instance.data = {f:self.cleaned_data.get(f,None) for f in self.extra_fields}
    instance.document = self.document
    if commit:
      instance.save()
    return instance
  class Meta:
    model = Signature
    exclude = ('datetime','status','status_changed','user','data')
