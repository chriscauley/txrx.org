from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models

from lablackey.db.models import UserModel
from lablackey.unrest import JsonMixin
from lablackey.contenttypes import get_contenttype

from jsonfield import JSONField

class Follow(UserModel):
  content_type = models.ForeignKey("contenttypes.ContentType")
  object_id = models.IntegerField()
  content_object = GenericForeignKey('content_type', 'object_id')
  datetime = models.DateTimeField(auto_now_add=True)
  __unicode__ = lambda self: "%s follows %s"%(self.user,self.content_object)
  json_fields = ('name','url','unfollow_url')
  name = property(lambda self: unicode(self.content_object))
  url = property(lambda self: self.content_object.get_absolute_url and self.content_object.get_absolute_url())
  unfollow_url = property(lambda self: reverse("notify_unfollow",args=[self.id]))
  def notify(self,**kwargs):
    return Notification.objects.get_or_create(
      follow=self,
      user=self.user,
      **kwargs
    )[0]
  class Meta:
    unique_together = ('user','content_type','object_id')
    ordering = ("-datetime",)

def get_model(s):
  app_label,model_name = s.split(".")
  return apps.get_app_config(app_label).get_model(model_name)

class Notification(UserModel,JsonMixin):
  follow = models.ForeignKey(Follow)
  datetime = models.DateTimeField(auto_now_add=True)
  emailed = models.DateTimeField(null=True,blank=True)
  read = models.DateTimeField(null=True,blank=True)
  message = models.CharField(max_length=512)
  data = JSONField(default=dict,blank=True)
  url = models.CharField(max_length=256,null=True,blank=True)
  __unicode__ = lambda self: "%s: %s"%(self.user,self.message)
  target_type = models.CharField(max_length=201,null=True,blank=True)
  target_id = models.IntegerField(null=True,blank=True)
  _get_target = lambda self: get_model(self.target_type).objects.get(pk=self.target_id)
  json_fields = ['follow','datetime','read','message','data','url','target_type','target_id']
  def row_permissions(self,user):
    return self.user == user
  def _set_target(self,obj):
    self.target_type = "%s.%s"%(obj._meta.app_label,obj._meta.model_name)
    self.target_id = obj.id
  target = property(_get_target,_set_target)
  class Meta:
    ordering = ("-datetime",)
