from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import models

class ContactPerson(models.Model):
  user = models.ForeignKey(get_user_model(),null=True,blank=True)
  _ht = "Use if desired email is not in a user account. THIS FIELD DOES NOTHING IF THERE IS A USER"
  email = models.EmailField(null=True,blank=True,help_text=_ht)
  __unicode__ = lambda self: str(self.user or self.email)
  def get_email(self):
    return self.user.email if (self.user and self.user.email) else self.email
  class Meta:
    verbose_name = "Person"

class ContactSubject(models.Model):
  subject = models.CharField(max_length=128)
  contactperson = models.ForeignKey(ContactPerson)
  __unicode__ = lambda self: self.subject
  get_email = lambda self: self.contactperson.get_email()
  class Meta:
    verbose_name = "Subject"

class ContactMessage(models.Model):
  from_name = models.CharField("Name",max_length=128)
  from_email = models.EmailField("Email")
  contactsubject = models.ForeignKey(ContactSubject,verbose_name="Subject")
  message = models.TextField()
  user = models.ForeignKey(get_user_model(),null=True,blank=True)
  __unicode__ = lambda self: "%s: %s"%(self.user or self.from_email,self.subject)
  subject = property(lambda self: self.contactsubject.subject)
  def save(self,*args,**kwargs):
    send_email = not self.pk
    super(ContactMessage,self).save(*args,**kwargs)
    if send_email:
      self.send()
  def send(self):
    send_mail(self.subject,"Message from: %s\n\n%s"%(self.from_name,self.message),
              self.from_email,[self.contactsubject.get_email()])
  class Meta:
    verbose_name = "Message"
