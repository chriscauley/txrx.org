from django.conf import settings
from django.db import models

class Question(models.Model):
  name = models.CharField(max_length=64)
  data = models.TextField()

class UserAnswer(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  question = models.ForeignKey(Question)
  data = models.TextField()
  __unicode__ = lambda self: "%s answers %s"%(self.user,self.question)
