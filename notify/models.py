from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from lablackey.db.models import UserModel
from lablackey.contenttypes import get_contenttype
from course.models import Session, Course

from jsonfield import JSONField

class NotifyCourse(UserModel):
  course = models.ForeignKey(Course)
  __unicode__ = lambda self: "{} -- {}".format(self.user,self.course)
  class Meta:
    unique_together = ('course','user')

class Follow(UserModel):
  content_type = models.ForeignKey("contenttypes.ContentType")
  object_id = models.IntegerField()
  content_object = GenericForeignKey('content_type', 'object_id')
  datetime = models.DateTimeField(auto_now_add=True)
  __unicode__ = lambda self: "%s follows %s"%(self.user,self.content_object)
  class Meta:
    unique_together = ('user','content_type','object_id')
    ordering = ("-datetime",)

class Notification(UserModel):
  follow = models.ForeignKey(Follow)
  datetime = models.DateTimeField(auto_now_add=True)
  read = models.DateTimeField(null=True,blank=True)
  message = models.CharField(max_length=512)
  data = JSONField(default=dict,blank=True)
  url = models.CharField(max_length=256,null=True,blank=True)
  __unicode__ = lambda self: "%s: %s"%(self.user,self.message)
  class Meta:
    ordering = ("-datetime",)
