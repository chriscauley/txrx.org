from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import render_to_string

from lablackey.db.models import NamedTreeModel
from lablackey.decorators import cached_property, cached_method
from media.models import PhotosMixin

from sorl.thumbnail import get_thumbnail
from course.models import CourseEnrollment
from crop_override import get_override
from drop.models import Product

import os, json

class BaseProduct(PhotosMixin,Product):
  #! TODO make this go to a filtered version of shop
  get_absolute_url = lambda self: "/shop/"
  json_fields = Product.json_fields + ['thumbnail','category_ids']
  class Meta:
    abstract = True
  @property
  def category_ids(self):
    return list(self.categories.all().values_list('id',flat=True)) + getattr(self,"base_categories",[])

class CourseCheckout(BaseProduct):
  json_fields = BaseProduct.json_fields + ['course_id']
  course = models.ForeignKey("course.Course")
  _ht = "Select the studio hours that can be picked for this checkout."
  _lct = { 'access_id': 4 }
  events = models.ManyToManyField("event.Event",limit_choices_to=_lct,help_text=_ht)
  base_categories = [1]
  get_name = lambda self: "%s (check-out test)"%self.name
  in_stock = property(lambda self: 9999)
  extra_fields = ['eventoccurrence_id','display','no_edit']
  def purchase(self,order_item):
    ce,new = CourseEnrollment.objects.get_or_create(
      course=self.course,
      user=order_item.order.user,
      eventoccurrence_id=order_item.extra.get('eventoccurrence_id',None),
      defaults={'quantity': order_item.quantity},
    )
    self.save()
    order_item.extra['purchased_model'] = "course.CourseEnrollment"
    order_item.extra['purchased_pk'] = ce.pk
    order_item.save()

class Consumable(BaseProduct):
  json_fields = BaseProduct.json_fields + ['in_stock'] #! TODO should be a boolean... is_in_stock or something
  part_number = models.CharField(max_length=32,null=True,blank=True)
  part_style = models.CharField(max_length=32,null=True,blank=True)
  purchase_url = models.URLField(max_length=1024,null=True,blank=True)
  purchase_url2 = models.URLField(max_length=1024,null=True,blank=True)
  _ht = "Leave blank and this fill always show as in stock."
  in_stock = models.IntegerField(null=True,blank=True,help_text=_ht)
  has_quantity = True
  _ht2 = "Amount purchased (by us when restocking) at a time. Used to make the refill process quick."
  purchase_quantity = models.IntegerField(default=1,help_text=_ht2)
  def purchase(self,order_item):
    if self.in_stock is None:
      return
    self.in_stock = self.in_stock- order_item.quantity
    self.save()
  def get_domain(self,attr):
    if not getattr(self,attr):
      return
    return getattr(self,attr).split('//')[-1].split('/')[0].split('.')[-2]
  purchase_domain = property(lambda self: self.get_domain('purchase_url'))
  purchase_domain2 = property(lambda self: self.get_domain('purchase_url2'))
  class Meta:
    ordering = ('name',)

class ToolConsumableGroup(models.Model):
  name = models.CharField(max_length=64)
  tools = models.ManyToManyField("tool.Tool")
  consumables = models.ManyToManyField(Consumable)
  __unicode__ = lambda self: self.name
  class Meta:
    ordering = ('name',)
