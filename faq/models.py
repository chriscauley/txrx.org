from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from wmd.models import MarkDownField

class Topic(models.Model):
  content_type = models.ForeignKey("contenttypes.ContentType")
  object_id = models.IntegerField()
  content_object = generic.GenericForeignKey('content_type', 'object_id')
  __unicode__ = lambda self: "%s (%s)"%(content_object,content_type)

class Question(models.Model):
  topic = models.ForeignKey(Topic)
  question = models.CharField(max_length=256)
  answer = MarkDownField(blank=True,null=True)
  order = models.IntegerField(default=9999999)
  created = models.DateField(auto_now_add=True)
  modified = models.DateField(auto_now=True)
  __unicode__ = lambda self: self.question
  class Meta:
    ordering = ('order',)
  
