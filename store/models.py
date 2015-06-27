from django.db import models

from db.models import NamedTreeModel
from media.models import PhotosMixin

from shop.models import Product

class Category(NamedTreeModel):
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
    class Meta:
        ordering = ('name',)
