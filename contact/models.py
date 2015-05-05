from django.conf import settings
from django.core.mail import send_mail
from django.db import models

class Person(models.Model):
  user = models.ForeignKey(get_user_model(),null=True,blank=True)
  _ht = "Use if desired email is not in a user account. THIS FIELD DOES NOTHING IF THERE IS A USER"
  email = models.EmailField(null=True,blank=True,help_text=_ht)
  __unicode__ = lambda self: str(self.user or self.email)
  def get_email(self):
    return self.user.email if (self.user and self.user.email) else self.email
  class Meta:
    verbose_name = "Person"

class Subject(models.Model):
  subject = models.CharField(max_length=128)
  person = models.ForeignKey(Person)
  order = models.IntegerField(default=9999)
  slug = models.CharField(max_length=32)
  __unicode__ = lambda self: self.subject
  faqs = property(lambda self: [s.faq for s in self.subjectfaq_set.all()])
  get_email = lambda self: self.person.get_email()
  class Meta:
    verbose_name = "Subject"
    ordering = ("order",)

class FAQ(models.Model):
  question = models.TextField(null=True,blank=True)
  answer = models.TextField()
  __unicode__ = lambda self: self.question or "(no question) %s..."%(answer[:50])

class SubjectFAQ(models.Model):
  subject = models.ForeignKey(Subject)
  faq = models.ForeignKey(FAQ)
  order = models.IntegerField(default=0)
  class Meta:
    ordering = ('order',)

class Message(models.Model):
  from_name = models.CharField("Name",max_length=128)
  from_email = models.EmailField("Email")
  subject = models.ForeignKey(Subject)
  message = models.TextField()
  user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True)
  __unicode__ = lambda self: "%s: %s"%(self.user or self.from_email,self.subject)
  def save(self,*args,**kwargs):
    send_email = not self.pk
    super(Message,self).save(*args,**kwargs)
    if send_email:
      self.send()
  def send(self):
    send_mail(self.subject,"Message from: %s\n\n%s"%(self.from_name,self.message),
              self.from_email,[self.subject.get_email()])
  class Meta:
    verbose_name = "Message"
