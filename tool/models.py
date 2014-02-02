from django.db import models
from django.conf import settings
from django.contrib.contenttypes import generic

from south.modelsinspector import add_introspection_rules
from wmd.models import MarkDownField
from codrspace.models import Photo

from db.models import SlugModel, OrderedModel
from txrx.utils import cached_property, cached_method

from tagging.fields import TagField

add_introspection_rules([], ["^wmd\.models\.MarkDownField"])

class Lab(SlugModel,OrderedModel):
  photo = models.ForeignKey(Photo,null=True,blank=True)
  description = models.TextField(null=True,blank=True)
  class Meta:
    ordering = ("order",)

_help = "Will default to %s photo if blank"

class Tool(SlugModel,OrderedModel):
  lab = models.ForeignKey(Lab)
  make = models.CharField(max_length=64,null=True,blank=True)
  model = models.CharField(max_length=32,null=True,blank=True)
  description = MarkDownField(blank=True,null=True)
  photo = models.ForeignKey(Photo,null=True,blank=True)
  links = lambda self: self.toollink_set.all()
  est_price = models.FloatField(null=True,blank=True)
  tags = TagField()
  class Meta:
    ordering = ("order",)

class ToolLink(OrderedModel):
  tool = models.ForeignKey(Tool)
  title = models.CharField(max_length=64)
  url = models.URLField(verify_exists=False)
  __unicode__ = lambda self: self.title
  class Meta:
    ordering = ("order",)

# This and ToolsMixin could probably be combined into some sort of generic foreign key factory
class TaggedTool(models.Model):
  tool = models.ForeignKey(Tool)
  content_type = models.ForeignKey("contenttypes.ContentType")
  object_id = models.IntegerField()
  content_object = generic.GenericForeignKey('content_type', 'object_id')
  order = models.IntegerField(default=9999)

class ToolsMixin():
  @cached_property
  def first_tool(self):
    return self.get_tools()[0]
  @cached_property
  def _ct_id(self):
    return ContentType.objects.get_for_model(self.__class__).id
  @cached_method
  def get_tools(self):
    return self._get_tools()
  def _get_tools(self):
    return list(Tool.objects.filter(taggedtool__content_type_id=self._ct_id,
                                     taggedtool__object_id=self.id).order_by("taggedtool__order"))
