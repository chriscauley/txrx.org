from django.conf import settings
from django.db import models
import jsonfield

class RFID(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  number = models.CharField(max_length=16,unique=True)
  added = models.DateTimeField(auto_now_add=True)
  __str__ = lambda self: "%s (%s)"%(self.user,self.number)
import jsonfield
class RFIDLog(models.Model):
  rfid_number = models.CharField(max_length=16)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True,blank=True)
  datetime = models.DateTimeField(auto_now_add=True)
  data = jsonfield.JSONField(default=dict)
  __str__ = lambda self: "%s@%s"%(self.rfid_number,self.datetime)
  def save(self,*args,**kwargs):
    # if this is new, save add a matching user, if any
    if not self.pk and RFID.objects.filter(number=self.rfid_number):
      self.user = RFID.objects.get(number=self.rfid_number).user
    super().save(*args,**kwargs)
