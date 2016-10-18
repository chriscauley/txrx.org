from django.db import models
from lablackey.db.models import OrderedModel

from django.contrib.flatpages.models import FlatPage

class Rate(models.Model):
  text = models.CharField(max_length=128)
  __unicode__ = lambda self: self.text
  class Meta:
    ordering = ('text',)

class FlatPagePrice(OrderedModel):
  flatpage = models.ForeignKey(FlatPage)
  name = models.CharField(max_length=128)
  member_rate = models.ForeignKey(Rate,related_name="+")
  nonmember_rate = models.ForeignKey(Rate,related_name="+")
  class Meta:
    ordering = ('order',)
