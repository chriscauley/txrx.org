from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify

from lablackey.db.models import UserModel,NamedTreeModel
from media.models import PhotosMixin, FilesMixin
from tool.models import ToolsMixin
from blog.templatetags.short_codes import explosivo

from wmd import models as wmd_models

class Material(NamedTreeModel):
  count = lambda self: self.thing_set.count()
  value = property(lambda self: self.pk)
  class Meta:
    ordering = ('order',)

class Thing(PhotosMixin,ToolsMixin,FilesMixin,UserModel):
  user_can_edit = True
  feed_item_type = 'thing'
  title = models.CharField(max_length=128)
  description = wmd_models.MarkDownField(blank=True,null=True)
  publish_dt = models.DateTimeField(auto_now_add=True)
  featured = models.BooleanField(default=False)
  active = models.BooleanField(default=False)
  parent_link = models.URLField(null=True,blank=True)
  parent = models.ForeignKey("self",null=True,blank=True)
  materials = models.ManyToManyField(Material,blank=True)
  session = models.ForeignKey('course.Session',null=True,blank=True)

  __unicode__ = lambda self: self.title
  get_absolute_url = lambda self: reverse('thing_detail',args=[self.id,slugify(self.title)])
  get_short_description = lambda self: self.description
  related_by_user = lambda self: Thing.objects.filter(user=self.user).exclude(pk=self.pk)
  def get_parent_text(self):
    if "thingiverse.com" in self.parent_link:
      return "View on Thingiverse!"
    return "View on %s"%(self.parent_link.split("//")[-1].split('/')[0].split('www.')[-1])
  class Meta:
    ordering = ('-publish_dt',)
