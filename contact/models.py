from django.conf import settings
from django.core.mail import send_mail
from django.db import models

import markdown

class Person(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True)
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
  read_count = models.IntegerField(default=0)
  marked_read = models.BooleanField(default=False)
  subject = models.ForeignKey(Subject)
  message = models.TextField()
  user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True)
  datetime = models.DateTimeField(auto_now_add=True)
  __unicode__ = lambda self: "%s: %s"%(self.user or self.from_email,self.subject)
  pixel_code = property(lambda self: "course.message_%s-%s"%(self.id,self.datetime))
  def get_tracking_pixel(self):
    return "<img src='%s.png'>"%(settings.SITE_URL+"/contact/"+self.pixel_code)
  def save(self,*args,**kwargs):
    send_email = not self.pk
    super(Message,self).save(*args,**kwargs)
    if send_email:
      self.send()
  def send(self):
    text = "Message from: %s\n\n%s"%(self.from_name,self.message)
    send_mail(
      "%s from %s"%(self.subject,self.from_name),
      text,
      self.from_email,
      [self.subject.get_email()],
      html_message=markdown.markdown(text)+self.get_tracking_pixel()
    )
  class Meta:
    verbose_name = "Message"
