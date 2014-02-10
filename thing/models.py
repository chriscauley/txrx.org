from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify

from db.models import UserModel
from codrspace.models import PhotosMixin
from tool.models import ToolsMixin

from wmd import models as wmd_models

class Material(models.Model):
  name = models.CharField(max_length=64)
  __unicode__ = lambda self: self.name
  class Meta:
    ordering = ('name',)

class Thing(UserModel,PhotosMixin,ToolsMixin):
  feed_item_type = 'thing'
  title = models.CharField(max_length=128)
  description = wmd_models.MarkDownField(blank=True,null=True)
  publish_dt = models.DateTimeField(auto_now_add=True)
  featured = models.BooleanField(default=False)
  active = models.BooleanField(default=False)
  parent_link = models.URLField(null=True,blank=True)
  parent = models.ForeignKey("self",null=True,blank=True)
  materials = models.ManyToManyField(Material,null=True,blank=True)

  __unicode__ = lambda self: self.title
  get_absolute_url = lambda self: reverse('thing_detail',args=[self.id,slugify(self.title)])
  related_by_user = lambda self: Thing.objects.filter(user=self.user).exclude(pk=self.pk)
  class Meta:
    ordering = ('-publish_dt',)
