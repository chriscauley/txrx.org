from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.db import models

from lablackey.utils import cached_method
from tool.models import CriterionModel
import json

class Document(models.Model):
  name = models.CharField(max_length=512)
  content = models.TextField(null=True,blank=True)
  _ht = "If checked, user must log into site before viewing/signing document"
  login_required = models.BooleanField(default=False,help_text=_ht)
  signature_required = models.BooleanField(default=True)
  __unicode__ = lambda self: self.name
  get_absolute_url = lambda self: reverse('signed_document',args=[self.id,slugify(self.name)])
  fields_json = property(lambda self: [f.as_json for f in self.documentfield_set.all()])

class Signature(CriterionModel):
  document = models.ForeignKey(Document)
  automatic = True
  date_typed = models.CharField("Type Todays Date",max_length=64,null=True,blank=True)
  name_typed = models.CharField("Type Your Name",max_length=128,null=True,blank=True)
  signature = models.ImageField(upload_to="signatures/%m-%d-%y",null=True,blank=True)
  user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True)
  data = models.TextField(null=True,blank=True)
  get_criteria = lambda self: self.document.criterion_set.all()
  __unicode__ = lambda self: "%s: %s - %s"%(self.document,self.name_typed,self.date_typed)
  def get_fields(self):
    fields = self.document.fields_json
    data = json.loads(self.data or '{}')
    for field in fields:
      field['value'] = data.get(field['slug'],None)
    return fields
  @property
  def as_json(self):
    return {
      'id': self.id,
      'document_name': unicode(self.document),
      'completed': unicode(self.completed or ''),
    }

INPUT_TYPE_CHOICES = [
  ('text','Text'),
  ('number','Number'),
  ('phone','Phone'),
  ('email','Email'),
  ('header','Design Element (non-input)'),
  ('select','Select'),
]

class DocumentField(models.Model):
  document = models.ForeignKey(Document)
  name = models.CharField(max_length=64)
  slug = models.CharField(max_length=64,help_text="For fields with the same name",null=True,blank=True)
  order = models.IntegerField(default=999)
  input_type = models.CharField(max_length=64,choices=INPUT_TYPE_CHOICES)
  choices = models.TextField(null=True,blank=True,help_text="Javascript array object for choice fields.")
  required = models.BooleanField(default=False)
  __unicode__ = lambda self: "%s for %s"%(self.slug or self.name,self.document)
  def get_options(self,choices=None):
    # valid choices are [[VALUE_1,VERBOSE_1],...] or [VERBOSE_1,...]
    if not self.choices:
      return
    choices = choices or json.loads(self.choices)
    return choices if isinstance(choices[0],list) else zip(choices,choices)
  @cached_method
  def get_optgroups(self):
    # returns None if self.choices is not in the optgroup format
    # optgroup format: [[OPTGROUP_NAME,[LISTOFCHOICES]]
    if not self.choices:
      return
    choices = json.loads(self.choices)
    if isinstance(choices[0],list) and isinstance(choices[0][1],list):
      return [[label,self.get_options(options)] for label,options in choices]
  @property
  def as_json(self):
    return {
      'name': self.name,
      'slug': self.slug or slugify(self.name),
      'type': self.input_type,
      'required': self.required,
      'choices': self.get_optgroups() or self.get_options()
    }
  class Meta:
    ordering = ('order',)
