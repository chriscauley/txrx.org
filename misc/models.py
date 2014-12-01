from django.db import models
from django.core.mail import EmailMessage

import datetime

class BulkEmail(models.Model):
  subject = models.CharField(max_length=128)
  body = models.TextField()
  send_on_save = models.BooleanField(default=False)
  __unicode__ = lambda self: self.subject

class BulkEmailRecipient(models.Model):
  bulkemail = models.ForeignKey(BulkEmail)
  email = models.EmailField()
  name = models.CharField(max_length=64)
  file1 = models.FileField(null=True,blank=True,upload_to="bulkemail")
  file2 = models.FileField(null=True,blank=True,upload_to="bulkemail")
  sent = models.DateTimeField(null=True,blank=True)
  def send(self):
    email = EmailMessage(
      self.bulkemail.subject,
      self.bulkemail.body,
      'txrxlabs@gmail.com',
      [self.email])
    if self.file1:
      email.attach_file(self.file1.path)
    if self.file2:
      email.attach_file(self.file2.path)
    email.send()
    self.sent = datetime.datetime.now()
    self.save()
