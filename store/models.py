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
  @property
  def as_json(self):
    image = get_thumbnail(get_override(self.first_photo,"landscape_crop"),"270x140",crop="center")
    return [
      self.pk,
      self.name,
      [image.width,image.height,image.url],
      [c.as_json for c in self.category_set.all()],
    ]
  #! TODO make this go to store filtered by category
  class Meta:
    verbose_name_plural = "Categories"
    ordering = ('order',)

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
  #! TODO make this go to a filtered version of shop
  get_absolute_url = lambda self: "/shop/"
  json_fields = Product.json_fields + ['thumbnail','category_ids']
  category_ids = property(lambda self: list(self.categories.all().values_list('id',flat=True)))
  @property
  def thumbnail(self):
    return get_thumbnail(get_override(self.first_photo,"landscape_crop"),"270x140",crop="center").url
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

class TaggedConsumable(models.Model):
  consumable = models.ForeignKey(Consumable)
  content_type = models.ForeignKey("contenttypes.ContentType")
  object_id = models.IntegerField()
  content_object = GenericForeignKey('content_type', 'object_id')
  order = models.IntegerField(default=9999)

class ConsumablesMixin(object):
  def consumable_ids(self):
    return list(self.get_consumables().values_list("id",flat=True))
  @cached_property
  def first_consumable(self):
    return self.get_consumables()[0]
  @cached_property
  def _ct_id(self):
    return ContentType.objects.get_for_model(self.__class__).id
  @cached_method
  def get_consumables(self):
    return self._get_consumables()
  def _get_consumables(self):
    return Consumable.objects.filter(
      taggedconsumable__content_type_id=self._ct_id,
      taggedconsumable__object_id=self.id).order_by("taggedconsumable__order")
  class Meta:
    abstract = True

def reset_products_json():
  values = {
    'categories': json.dumps([c.as_json for c in Category.objects.all()]),
    'products': json.dumps([p.as_json for p in Consumable.objects.all()])
  }
  text = render_to_string('store/products.json',values)
  f = open(os.path.join(settings.STATIC_ROOT,'_products.json'),'w')
  f.write(text)
  f.close()
  os.rename(os.path.join(settings.STATIC_ROOT,'_products.json'),os.path.join(settings.STATIC_ROOT,'products.json'))
  return text
