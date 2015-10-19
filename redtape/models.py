from django.db import models

class Document(models.Model):
  name = models.CharField(max_length=64)
  content = models.TextField(null=True,blank=True)
  __unicode__ = lambda self: self.name

class Signature(models.Model):
  document = models.ForeignKey(Document)
  date_typed = models.CharField("Type Todays Date",max_length=64)
  name_typed = models.CharField("Type Your Name",max_length=128)
  signature = models.ImageField(upload_to="signatures/%m-%d-%y")
  date = models.DateField(auto_now_add=True)
  __unicode__ = lambda self: "%s - %s"%(self.name_typed,self.date_typed)
