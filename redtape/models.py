from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.forms import ValidationError
from django.template.defaultfilters import slugify

from lablackey.blog.templatetags.short_codes import explosivo
from lablackey.db.models import JsonMixin
from lablackey.decorators import cached_method

from media.models import UploadedFile
from tool.models import CriterionModel

import json, jsonfield

class Document(models.Model,JsonMixin):
  name = models.CharField(max_length=512)
  content = models.TextField(null=True,blank=True)
  _ht = "If checked, user must log into site before viewing/signing document"
  login_required = models.BooleanField(default=False,help_text=_ht)
  _ht = "After submitting the document can the creator edit it?" \
        "If false a new document will be created everytime they submit the document."
  editable = models.BooleanField(default=True,help_text=_ht)
  __unicode__ = lambda self: self.name
  get_absolute_url = lambda self: reverse('signed_document',args=[self.id,slugify(self.name)])
  fields_json = property(lambda self: [f.as_json for f in self.documentfield_set.all()])
  data_fields = property(lambda self: [f.get_name for f in self.documentfield_set.all()])
  rendered_content = property(lambda self: explosivo(self.content))
  def get_json_for_user(self,user):
    json = self.as_json
    try:
      signature = Signature.objects.get(user=user,document=self)
    except Signature.DoesNotExist:
      pass
    else:
      json['completed'] = signature.status == "completed"
    return json
  @property
  def as_json(self):
    return {
      'id': self.id,
      'name': self.name,
      'content': self.content,
      'rendered_content': self.rendered_content,
      'schema': self.fields_json,
    }

def signature_validator(value):
  value = str(value)
  if not value.lower().startswith("/s/"):
    raise ValidationError("Signature must start with /s/")

class Signature(CriterionModel):
  user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True)
  document = models.ForeignKey(Document)
  automatic = True
  _ht = 'You signature must start with a /s/. For example enter "/s/John Hancock" without the quotes.'
  data = jsonfield.JSONField(default=dict)
  get_criteria = lambda self: self.document.criterion_set.all()
  __unicode__ = lambda self: "%s: %s"%(self.document,self.user)
  def get_files(self):
    files = self.data.get("files",None)
    if not files:
      return
    return UploadedFile.objects.filter(id__in=files.split(","))
  def get_fields(self):
    fields = self.document.fields_json
    for field in fields:
      field['value'] = self.data.get(field['name'],None)
    return fields
  @property
  def as_json(self):
    return {
      'id': self.id,
      'document_name': unicode(self.document),
      'completed': self.status == "completed",
    }

INPUT_TYPE_CHOICES = [
  ('text','Text'),
  ('textarea','Textarea (multi-line)'),
  ('number','Number'),
  ('phone','Phone'),
  ('email','Email'),
  ('header','Design Element (non-input)'),
  ('checkbox','Checkbox'),
  ('select','Select'),
  ('checkbox-input','Select Multiple'),
  ('signature','Sign Your Name'),
  ('multi-file','Multiple File'),
  ('services','"Services"'),
]

INPUT_TYPE_MAP = {
  'phone': 'text'
}

INPUT_HELP_TEXT = {
  'signature': 'Signed name should start with /s/, eg /s/John Hancock'
}

class DocumentField(models.Model):
  document = models.ForeignKey(Document)
  label = models.CharField(max_length=64)
  name = models.CharField(max_length=64,help_text="For fields with the same label",null=True,blank=True)
  order = models.IntegerField(default=999)
  input_type = models.CharField(max_length=64,choices=INPUT_TYPE_CHOICES)
  _ht = "Json object for field generation. Will overwrite any other database entry (name, label, etc.)"
  data = jsonfield.JSONField(default=dict,blank=True,help_text=_ht)
  required = models.BooleanField(default=False)
  __unicode__ = lambda self: "%s for %s"%(self.label,self.document)
  get_name = lambda self: self.name or slugify(self.label)
  @property
  def as_json(self):
    data = {
      'label': self.label,
      'name': self.get_name(),
      'type': INPUT_TYPE_MAP.get(self.input_type,self.input_type),
      'required': self.required,
      'help_text': INPUT_HELP_TEXT.get(self.input_type,None),
    }
    data.update(self.data.copy())
    if self.input_type == "services":
      data['choices'] = []
      data['member_choices'] = []
      for service in Service.objects.all():
        data['choices'].append([slugify(service.name),service.get_display_name()])
        data['member_choices'].append([slugify(service.name),service.get_member_display_name()])
      data['type'] = 'checkbox-input'
    return data
  class Meta:
    ordering = ('order',)

class Service(models.Model):
  name = models.CharField(max_length=32)
  price = models.IntegerField(default=0)
  member_price = models.IntegerField(default=0)
  order = models.IntegerField(default=0)
  __unicode__ = lambda self: self.name
  def get_display_name(self):
    if not self.price:
      return self.name
    return "%s ($%s/hr)"%(self.name,self.price)
  def get_member_display_name(self):
    if not self.member_price:
      return self.name
    return "%s ($%s/hr)"%(self.name,self.member_price)
  class Meta:
    ordering = ('order',)
