from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string

from db.models import NamedTreeModel
from media.models import PhotosMixin

from sorl.thumbnail import get_thumbnail
from crop_override import get_override
from shop.models import Product

import os, json

class Category(PhotosMixin,NamedTreeModel):
  @property
  def as_json(self):
    image = get_thumbnail(get_override(self.first_photo,'landscape_crop'),"298x199",crop="center")
    return [
      self.pk,
      self.name,
      [image.width,image.height,image.url],
      [c.as_json for c in self.category_set.all()],
    ]
  class Meta:
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
  def decrease_stock(self,quantity):
    if self.in_stock is None:
      return
    self.in_stock = max(self.in_stock- quantity,0)
  @property
  def as_json(self):
    image = get_thumbnail(get_override(self.first_photo,'landscape_crop'),"298x199",crop="center")
    return [
      self.pk,
      self.name,
      [image.width,image.height,image.url],
      int(100*self.unit_price),
      [c.pk for c in self.categories.all()],
      self.in_stock
    ]
  def get_domain(self,attr):
    if not getattr(self,attr):
      return
    return getattr(self,attr).split('//')[-1].split('/')[0].split('.')[-2]
  purchase_domain = property(lambda self: self.get_domain('purchase_url'))
  purchase_domain2 = property(lambda self: self.get_domain('purchase_url2'))
  def save(self,*args,**kwargs):
    self.slug = slugify(self.name)
    super(Consumable,self).save(*args,**kwargs)
  get_absolute_url = lambda self: reverse('product_detail',args=[self.pk,self.slug])
  class Meta:
    ordering = ('name',)

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
