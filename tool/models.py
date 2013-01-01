from django.db import models
from django.conf import settings

from south.modelsinspector import add_introspection_rules
from wmd.models import MarkDownField
from codrspace.models import Media

from lablackey.db.models import SlugModel, OrderedModel
from lablackey.utils import cached_method

add_introspection_rules([], ["^wmd\.models\.MarkDownField"])

class Lab(SlugModel,OrderedModel):
  photo = models.ForeignKey(Media,null=True,blank=True)
  description = models.TextField(null=True,blank=True)
  class Meta:
    ordering = ("order",)

_help = "Will default to %s photo if blank"

class Tool(SlugModel,OrderedModel):
  lab = models.ForeignKey(Lab)
  make = models.CharField(max_length=64,null=True,blank=True)
  model = models.CharField(max_length=32,null=True,blank=True)
  description = MarkDownField(blank=True,null=True)
  photo = models.ForeignKey(Media,null=True,blank=True)
  links = lambda self: self.toollink_set.all()
  class Meta:
    ordering = ("order",)

class ToolLink(OrderedModel):
  tool = models.ForeignKey(Tool)
  title = models.CharField(max_length=64)
  url = models.URLField(verify_exists=False)
  __unicode__ = lambda self: self.title
  class Meta:
    ordering = ("order",)
