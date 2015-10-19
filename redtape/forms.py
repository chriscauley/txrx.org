from django import forms
from django.core.files import File
from django.template.defaultfilters import slugify

from .models import Signature, Document

from jsignature.forms import JSignatureField
from jsignature.utils import draw_signature

class SignatureForm(forms.ModelForm):
  document = forms.ModelChoiceField(Document.objects.all(),widget=forms.HiddenInput())
  _signature = JSignatureField(label="Sign Your Name")
  def save(self,*args,**kwargs):
    commit = kwargs.pop("commit",True)
    kwargs['commit'] = False
    instance = super(SignatureForm,self).save(*args,**kwargs)
    signature = draw_signature(self.cleaned_data.get('_signature'),as_file=True)
    fname = "%s.png"%slugify(self.cleaned_data['name_typed'])
    instance.signature.save(fname,File(open(signature)))
    if commit:
      instance.save()
    return instance
  class Meta:
    model = Signature
    fields = ('document','date_typed','name_typed','_signature')
