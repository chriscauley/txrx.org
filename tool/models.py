from django.db import models
from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from db.models import SlugModel, OrderedModel
from media.models import Photo, PhotosMixin
from main.utils import cached_property, cached_method
from wmd.models import MarkDownField
from geo.models import Room

class Lab(PhotosMixin,OrderedModel):
  name = models.CharField(max_length=128)
  __unicode__ = lambda self: self.name
  slug = property(lambda self: slugify(self.name))
  photo = models.ForeignKey(Photo,null=True,blank=True)
  description = models.TextField(null=True,blank=True)
  url = lambda self: reverse("lab_detail",args=[self.slug,self.id])
  class Meta:
    ordering = ("order",)

_help = "Will default to %s photo if blank"

class Tool(PhotosMixin,OrderedModel):
  name = models.CharField(max_length=128)
  __unicode__ = lambda self: self.name
  value = property(lambda self: self.pk)
  slug = property(lambda self: slugify(self.name))
  lab = models.ForeignKey(Lab)
  make = models.CharField(max_length=64,null=True,blank=True)
  model = models.CharField(max_length=32,null=True,blank=True)
  description = MarkDownField(blank=True,null=True)
  est_price = models.FloatField(null=True,blank=True)
  links = lambda self: self.toollink_set.all()
  materials = models.ManyToManyField("thing.Material",null=True,blank=True)
  room = models.ForeignKey(Room,null=True,blank=True)
  get_absolute_url = lambda self: reverse("tool_detail",args=[self.slug,self.id])
  functional = models.BooleanField(default=True)
  repair_date = models.DateField(null=True,blank=True)
  get_status = lambda self: "Functional" if self.functional else "Non-functional"
  class Meta:
    ordering = ("lab","order")
  # Abstract the next two!
  @cached_property
  def courses(self):
    ct_id = ContentType.objects.get(name="course").id
    tagged = list(TaggedTool.objects.filter(content_type__id=ct_id,tool=self))
    return [t.content_object for t in tagged]
  @cached_property
  def things(self):
    ct_id = ContentType.objects.get(name="thing").id
    tagged = list(TaggedTool.objects.filter(content_type__id=ct_id,tool=self))
    return [t.content_object for t in tagged]

class ToolLink(OrderedModel):
  tool = models.ForeignKey(Tool)
  title = models.CharField(max_length=64)
  url = models.URLField()
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

class ToolsMixin(object):
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
  class Meta:
    abstract = True

class ToolCertification(models.Model):
  name = models.CharField(max_length=32)
  tool = models.ForeignKey(Tool)
  safety = models.BooleanField(default=False)
  waiver = models.BooleanField(default=False)
  room = models.ForeignKey(Room)
