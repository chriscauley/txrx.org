from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.db import models
from django.forms import ValidationError
from django.template.defaultfilters import slugify

from lablackey.decorators import cached_method
from lablackey.unrest import JsonMixin
from lablackey.db.models import UserOrSessionMixin
from tool.models import CriterionModel

import json

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
  def get_json_for_user(self,user):
    json = self.as_json
    try:
      signature = Signature.objects.get(user=user,document=self)
    except Signature.DoesNotExist:
      pass
    else:
      json['completed'] = signature.completed
    return json
  @property
  def as_json(self):
    return {
      'id': self.id,
      'name': self.name,
      'content': self.content,
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
  data = models.TextField(null=True,blank=True)
  get_criteria = lambda self: self.document.criterion_set.all()
  __unicode__ = lambda self: "%s: %s"%(self.document,self.user)
  def get_files(self):
    files = json.loads(self.data).get("files",None)
    if not files:
      return
    return UploadedFile.objects.filter(id__in=files.split(","))

  def get_fields(self):
    fields = self.document.fields_json
    data = json.loads(self.data or '{}')
    for field in fields:
      field['value'] = data.get(field['name'],None)
    return fields
  @property
  def as_json(self):
    return {
      'id': self.id,
      'document_name': unicode(self.document),
      'completed': unicode(self.completed or ''),
    }

private_storage = FileSystemStorage(
  location=getattr(settings,"PRIVATE_ROOT",settings.MEDIA_ROOT),
  base_url=getattr(settings,"PRIVATE_URL","/redtape/file/")
)

class UploadedFile(models.Model,UserOrSessionMixin,JsonMixin):
  src = models.FileField(storage=private_storage,upload_to="%Y%m",max_length=200,null=True,blank=True)
  name = models.CharField(max_length=256)
  content_type = models.CharField(max_length=256)
  url = property(lambda self: self.src.url)
  __unicode__ = lambda self: self.name
  json_fields = ['id','name','url','content_type']

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
  choices = models.TextField(null=True,blank=True,help_text="Javascript array object for choice fields.")
  required = models.BooleanField(default=False)
  __unicode__ = lambda self: "%s for %s"%(self.label,self.document)
  def get_options(self,choices=None):
    # valid choices are [[VALUE_1,VERBOSE_1],...] or [VERBOSE_1,...]
    if not self.choices:
      return
    choices = choices or json.loads(self.choices)
    return choices if isinstance(choices[0],list) else zip(choices,choices)
  def get_input_type(self):
    return INPUT_TYPE_MAP.get(self.input_type,self.input_type)
  @cached_method
  def get_optgroups(self):
    # returns None if self.choices is not in the optgroup format
    # optgroup format: [[OPTGROUP_NAME,[LISTOFCHOICES]]
    if not self.choices:
      return
    choices = json.loads(self.choices)
    if isinstance(choices[0],list) and isinstance(choices[0][1],list):
      return [[label,self.get_options(options)] for label,options in choices]
  get_name = lambda self: self.name or slugify(self.label)
  @property
  def as_json(self):
    return {
      'label': self.label,
      'name': self.get_name(),
      'type': self.get_input_type(),
      'required': self.required,
      'choices': self.get_optgroups() or self.get_options(),
      'help_text': INPUT_HELP_TEXT.get(self.input_type,None),
    }
  class Meta:
    ordering = ('order',)
