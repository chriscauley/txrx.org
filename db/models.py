from django.db import models
from django.template.defaultfilters import slugify

class OrderedModel(models.Model):
  order = models.PositiveIntegerField(default=99999)
  def save(self,*args,**kwargs):
    if self.order == 99999:
      self.order = 0
      if self.__class__.objects.count():
        self.order = self.__class__.objects.order_by("-order")[0].order+1
    super(OrderedModel,self).save(*args,**kwargs)
  class Meta:
    abstract = True

class SlugModel(models.Model):
  title = models.CharField(max_length=128)
  __unicode__ = lambda self: self.title
  slug = models.CharField(max_length=128,null=True,blank=True,unique=True)
  def save(self,*args,**kwargs):
    self.slug = slugify(self.title)
    if self.__class__.objects.filter(slug=self.slug).exclude(id=self.id):
      self.slug += "-%s"%self.id
    return super(SlugModel,self).save(*args,**kwargs)
  class Meta:
    abstract = True

class ColumnModel(models.Model):
  choices = (('right','right'),('left','left'))
  column = models.CharField(max_length=8,choices=choices)
  class Meta:
    abstract = True
