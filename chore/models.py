from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import datetime

class Tag(models.Model):
  name = models.CharField(max_length=64, unique=True)
  slug = models.CharField(max_length=64, unique=True, null=True, blank=True)

  def save(self,*args,**kwargs):
    self.slug = slugify(self.name)
    return super(Tag,self).save(*args,**kwargs)
  __unicode__ = lambda self: self.name

class Task(models.Model):
  name = models.CharField(max_length=64)
  description = models.TextField()
  rtext = "Number of days between repeated events. Set to 0 to not repeat."
  repeat = models.IntegerField(help_text=rtext,default=0)
  dtext = "First date + time of repeat. Will be used to make the first occurrence."
  first_date = models.DateTimeField(help_text=dtext)
  tags = models.ManyToManyField(Tag,blank=True)
  __unicode__ = lambda self: self.name
  def save(self,*args,**kwargs):
    if not self.id:
      super(Task,self).save(*args,**kwargs)
      self.update_occurrences()
    return super(Task,self).save(*args,**kwargs)

  def update_occurrences(self):
    dt = self.first_date
    for i in range(20):
      offset = 0 
      if self.repeat:
        offset = max([(datetime.datetime.now()-dt).days,0])
        offset = offset/self.repeat
      kwargs = dict(task=self,datetime=dt+datetime.timedelta(self.repeat*(i+offset)))
      occ, new = Occurrence.objects.get_or_create(**kwargs)

class Occurrence(models.Model):
  task = models.ForeignKey(Task)
  datetime = models.DateTimeField("Due Date")
  comments = models.TextField(null=True,blank=True)
  complete = models.BooleanField(default=False)
  __unicode__ = lambda self: '"%s" on %s'%(self.task,self.datetime)
  user_ids = lambda self: [a.user__id for a in self.assignment_set.all()]
  class Meta:
    ordering = ("datetime",)

class Assignment(models.Model):
  occurrence = models.ForeignKey(Occurrence)
  user = models.ForeignKey(User)

class Completion(models.Model):
  occurrence = models.ForeignKey(Occurrence)
  user = models.ForeignKey(User)
  datetime = models.DateTimeField(auto_now_add=True)
