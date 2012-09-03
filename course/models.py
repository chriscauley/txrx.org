from django.db import models
from django.conf import settings
from lablackey.profile.models import UserModel
from sorl.thumbnail import ImageField
import datetime

from lablackey.geo.models import Location
from lablackey.event.models import Event
from articles.models import Tag
from tool.models import Tool

_desc_help = "Line breaks and html tags will be preserved. Use html with care!"

class Subject(models.Model):
  name = models.CharField(max_length=32)
  value = lambda self: self.name
  __unicode__ = lambda self: self.name
  class Meta:
    ordering = ('name',)

class Term(models.Model):
  name = models.CharField(max_length=32)
  start = models.DateField()
  end = models.DateField()
  __unicode__ = lambda self: self.name
  _s = lambda d: d.strftime("%Y%m%d")
  value = lambda self: self._s(self.start)+"|"+self._s(self.end)
  class Meta:
    ordering = ('-start',)

class Course(models.Model):
  name = models.CharField(max_length=64)
  subjects = models.ManyToManyField(Subject)
  _folder = settings.UPLOAD_DIR+'/course/%Y-%m'
  src = ImageField("Logo",max_length=300,upload_to=_folder,null=True,blank=True)
  __unicode__ = lambda self: self.name
  class Meta:
    ordering = ("name",)

class Section(models.Model):
  course = models.ForeignKey(Course)
  term = models.ForeignKey("Term")
  fee = models.IntegerField(null=True,blank=True)
  fee_notes = models.CharField(max_length=256,null=True,blank=True)
  requirements = models.CharField(max_length=256,null=True,blank=True)
  prerequisites = models.CharField(max_length=256,null=True,blank=True)
  description = models.TextField(null=True,blank=True)
  location = models.ForeignKey(Location,default=1)
  src = ImageField("Logo",max_length=300,upload_to='course/%Y-%m',null=True,blank=True)
  tools = models.ManyToManyField(Tool,blank=True)
  cancelled = models.BooleanField(default=False)
  max_students = models.IntegerField(default=40)
  closed = lambda self: self.cancelled or self.starttime>datetime.datetime.now()

  get_instructors = lambda self: set([s.user for s in self.session_set.all()])

  __unicode__ = lambda self: "%s - %s"%(self.course.name,self.term)
  class Meta:
    ordering = ("term","course")

class Session(UserModel):
  section = models.ForeignKey(Section)
  ts_help = "Only used to set dates on creation."
  time_string = models.CharField(max_length=128,help_text=ts_help,default='not implemented')
  __unicode__ = lambda self: "%s (%s)"%(self.section, self.user)
  def save(self,*args,**kwargs):
    from membership.models import Profile
    profile,new = Profile.objects.get_or_create(user=self.user)
    return super(Session,self).save(*args,**kwargs)
  def first_date(self):
    if self.classtime_set.count():
      return self.classtime_set.all()[0].start
    return 0

class ClassTime(models.Model):
  session = models.ForeignKey(Session)
  start = models.DateTimeField()
  end_time = models.TimeField()
  class Meta:
    ordering = ("start",)


class Enrollment(UserModel):
  session = models.ForeignKey(Session)




from paypal.signals import payment_was_successful, payment_was_flagged
from django.dispatch import receiver
from django.http import QueryDict
from django.contrib.auth.models import User


@receiver(payment_was_successful, dispatch_uid='course.signals.handle_successful_payment')
def handle_successful_payment(sender, **kwargs):
    print 'Got payment!'

    #see if the user exists
    email = sender.payer_email
    users = User.objects.filter(email=email)
    user_count = users.count()
    if user_count == 0:
        #create them
        user = User.objects.create_user(username=email, email=email)
        user.save()
        #TODO: send them a welcome message / password reset email
        #TODO: also subscribe them to the TX/RX announcements mailing list
    elif user_count == 1:
        #get them
        user = users[0]
    elif user_count > 1:
        #WE GOT PROBLEMS
        user = None

    #add them to the classes they're enrolled in
    params = QueryDict(sender.query)
    class_count = int(params.get('cart_items'))

    for i in range(1, class_count+1):
        session_id = params['item_number%d' % i]
        section_cost = int(params['mc_gross_%d' % i])

        session = Session.objects.get(id=session_id)

        #make sure they didn't spoof things to paypal
        if section_cost == session.section.fee:
            #everything is groovy
            enrollment = Enrollment(user=user, session=session)
            enrollment.save()

        else:
            #they tried to cheat us
            #email the admins
            pass




@receiver(payment_was_flagged, dispatch_uid='course.signals.handle_flagged_payment')
def handle_flagged_payment(sender, **kwargs):
    print 'Got payment!'

    #email people to let them intervene manually