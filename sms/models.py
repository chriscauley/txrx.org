from django.conf import settings
from django.db import models
from django.utils import timezone

from lablackey.db.models import UserModel

from twilio.rest import TwilioRestClient
import random, datetime

def send(body,to,from_=settings.TWILIO_NUMBER):
  client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)
  message = client.messages.create(to=to,from_=from_,body=body)

outbox = []

if settings.TESTING:
  class Message(object):
    body = to = from_  = None
  def send(body,to,from_):
    m = Message()
    m.body = body
    m.to = to
    m.from_ = from_
    outbox.push(m)

_digits = getattr(settings,"TWILIO_VERIFICATION_DIGITS",4)
_days = getattr(settings,"TWILIO_EXPIRATION_SECONDS",20*60)

def random_code():
  return random.randint(10**(_digits-1),10**_digits)
def expiry():
  return timezone.now()+datetime.timedelta(0,_days)

class SMSNumber(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL)
  number = models.CharField(max_length=16,unique=True)
  verified = models.DateTimeField(null=True,blank=True)
  code = models.IntegerField(default=random_code)
  expire = models.DateTimeField(default=expiry)
  def send_verification(self):
    self.code = random_code()
    self.expire = expiry()
    self.save()
    send("Code: %s for %s"%(self.code,settings.SITE_NAME),self.number)
  __unicode__ = lambda self: "%s - %s"%(self.number,self.user)
