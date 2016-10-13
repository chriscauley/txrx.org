from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import render_to_string

from lablackey.db.models import NamedTreeModel
from lablackey.utils import cached_property, cached_method
from media.models import PhotosMixin

from sorl.thumbnail import get_thumbnail
from crop_override import get_override
from drop.models import Product

import os, json

class Category(PhotosMixin,NamedTreeModel):
  json_fields = ['id','name']
  @property
  def as_json(self):
    return {k:getattr(self,k) for k in self.json_fields}
  #! TODO make this go to store filtered by category
  #! TODO I took out the first image from the json and the subcategories since they weren't being used
  class Meta:
    verbose_name_plural = "Categories"
    ordering = ('order',)

class BaseProduct(PhotosMixin,Product):
  #! TODO make this go to a filtered version of shop
  get_absolute_url = lambda self: "/shop/"
  json_fields = Product.json_fields + ['thumbnail','category_ids']
  class Meta:
    abstract = True
  @property
  def category_ids(self):
    return list(self.categories.all().values_list('id',flat=True)) + getattr(self,"base_categories",[])

  @property
  def thumbnail(self):
    return get_thumbnail(get_override(self.first_photo,"landscape_crop"),"270x140",crop="center").url

class CourseCheckout(BaseProduct):
  course = models.ForeignKey("course.Course")
  base_categories = [6]

class Consumable(PhotosMixin,Product):
  categories = models.ManyToManyField(Category)
  part_number = models.CharField(max_length=32,null=True,blank=True)
  part_style = models.CharField(max_length=32,null=True,blank=True)
  purchase_url = models.URLField(max_length=1024,null=True,blank=True)
  purchase_url2 = models.URLField(max_length=1024,null=True,blank=True)
  _ht = "Leave blank and this fill always show as in stock."
  in_stock = models.IntegerField(null=True,blank=True,help_text=_ht)
  _ht2 = "Amount purchased at a time. Used to make the quick refill process."
  purchase_quantity = models.IntegerField(default=1,help_text=_ht2)
  def decrease_stock(self,quantity):
    if self.in_stock is None:
      return
    self.in_stock = max(self.in_stock- quantity,0)
  def get_domain(self,attr):
    if not getattr(self,attr):
      return
    return getattr(self,attr).split('//')[-1].split('/')[0].split('.')[-2]
  purchase_domain = property(lambda self: self.get_domain('purchase_url'))
  purchase_domain2 = property(lambda self: self.get_domain('purchase_url2'))
  def save(self,*args,**kwargs):
    super(Consumable,self).save(*args,**kwargs)
  class Meta:
    ordering = ('name',)

class ToolConsumableGroup(models.Model):
  name = models.CharField(max_length=64)
  tools = models.ManyToManyField("tool.Tool")
  consumables = models.ManyToManyField(Consumable)
  __unicode__ = lambda self: self.name
  class Meta:
    ordering = ('name',)
