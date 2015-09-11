from django.conf import settings
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

def to_base32(s):
  key = '-abcdefghijklmnopqrstuvwxyz'
  s = s.strip('0987654321')
  return int("0x"+"".join([hex(key.find(i))[2:].zfill(2) for i in (slugify(s)+"----")[:4]]),16)

class NamedTreeModel(models.Model):
  name = models.CharField(max_length=64)
  parent = models.ForeignKey("self",null=True,blank=True)
  order = models.FloatField(default=0)
  def get_order(self):
    max_num = to_base32("zzzz")
    if self.parent:
      return to_base32(self.parent.name) + to_base32(self.name)/float(max_num)
    return to_base32(self.name)
  def save(self,*args,**kwargs):
    self.order = self.get_order()
    super(NamedTreeModel,self).save(*args,**kwargs)

  def __unicode__(self):
    if self.parent:
      return "(%s) %s"%(self.parent,self.name)
    return self.name
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

class UserModel(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  class Meta:
    abstract = True
