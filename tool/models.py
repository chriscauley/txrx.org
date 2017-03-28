from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string

from lablackey.db.models import SlugModel, OrderedModel
from lablackey.decorators import cached_property, cached_method
from media.models import Photo, PhotosMixin
from wmd.models import MarkDownField

from colorful.fields import RGBColorField
import json, os, datetime, string, random

class Lab(PhotosMixin,OrderedModel):
  name = models.CharField(max_length=128)
  __unicode__ = lambda self: self.name
  get_admin_url = lambda self: "/admin/tool/lab/%s/"%self.id
  slug = property(lambda self: slugify(self.name))
  photo = models.ForeignKey(Photo,null=True,blank=True)
  description = MarkDownField(null=True,blank=True)
  url = lambda self: reverse("lab_detail",args=[self.slug,self.id])
  class Meta:
    ordering = ("order",)

_help = "Will default to %s photo if blank"

class Tool(PhotosMixin,OrderedModel):
  name = models.CharField(max_length=128)
  __unicode__ = lambda self: self.name
  get_admin_url = lambda self: "/admin/tool/tool/%s/"%self.id
  value = property(lambda self: self.pk)
  slug = property(lambda self: slugify(self.name))
  lab = models.ForeignKey(Lab)
  make = models.CharField(max_length=64,null=True,blank=True)
  model = models.CharField(max_length=32,null=True,blank=True)
  description = MarkDownField(blank=True,null=True)
  est_price = models.FloatField(null=True,blank=True)
  links = lambda self: self.toollink_set.all()
  materials = models.ManyToManyField("thing.Material",blank=True)
  room = models.ForeignKey('geo.Room',null=True,blank=True)
  get_absolute_url = lambda self: reverse("tool_detail",args=[self.slug,self.id])
  functional = models.BooleanField(default=True)
  repair_date = models.DateField(null=True,blank=True)
  permission = models.ForeignKey("Permission",null=True,blank=True)
  get_status = lambda self: "Functional" if self.functional else "Non-functional"
  @cached_property
  def consumable_ids(self):
    return list(self.toolconsumablegroup_set.values_list("consumables__id",flat=True))
  @cached_property
  def checkoutitems(self):
    ids = self.toolcheckoutitemgroup_set.values_list("checkoutitems",flat=True)
    return CheckoutItem.objects.filter(id__in=ids)
  @property
  def choice_name(self):
    if self.room:
      return "(%s) %s"%(self.room.name,self.name)
    return self.name
  class Meta:
    ordering = ("lab","order")
  # Abstract the next two!
  @cached_property
  def courses(self):
    ct_id = ContentType.objects.get(model="course").id
    tagged = list(TaggedTool.objects.filter(content_type__id=ct_id,tool=self))
    return [t.content_object for t in tagged]
  @cached_property
  def ordered_courses(self):
    singles = []
    groups = []
    if self.permission:
      for criterion in self.permission.criteria.all():
        if criterion.courses.count() == 1:
          singles.append(criterion.courses.all()[0])
        elif criterion.courses.all():
          groups.append(criterion.courses.all())
    return singles,groups
  single_courses = property(lambda self: self.ordered_courses[0])
  group_courses = property(lambda self: self.ordered_courses[1])
  number_required_courses = property(lambda self: len(self.single_courses) + len(self.group_courses))
  @cached_property
  def things(self):
    ct_id = ContentType.objects.get(model="thing").id
    tagged = list(TaggedTool.objects.filter(content_type__id=ct_id,tool=self))
    return [t.content_object for t in tagged]
  @property
  def as_json(self):
    fields = ['id','name']
    return {field:getattr(self,field) for field in fields}

class ToolLink(OrderedModel):
  tool = models.ForeignKey(Tool)
  title = models.CharField(max_length=64)
  url = models.URLField()
  __unicode__ = lambda self: self.title
  class Meta:
    ordering = ("order",)

# This and ToolsMixin could probably be combined into some sort of generic foreign key factory
class TaggedTool(models.Model):
  tool = models.ForeignKey(Tool)
  content_type = models.ForeignKey("contenttypes.ContentType")
  object_id = models.IntegerField()
  content_object = GenericForeignKey('content_type', 'object_id')
  order = models.IntegerField(default=9999)

class ToolsMixin(object):
  @cached_property
  def first_tool(self):
    return self.get_tools()[0]
  @cached_property
  def _ct_id(self):
    return ContentType.objects.get_for_model(self.__class__).id
  @cached_method
  def get_tools(self):
    return self._get_tools()
  def _get_tools(self):
    return list(Tool.objects.filter(
      taggedtool__content_type_id=self._ct_id,
      taggedtool__object_id=self.id).order_by("taggedtool__order"))
  class Meta:
    abstract = True

class Criterion(models.Model):
  name = models.CharField(max_length=32)

  # These fields will eventually need to be a generic many to many field but we don't have a ui for that
  _help_template = 'If a user %s and then is marked "complete", this criteria will be granted to that user.'
  _ht = _help_template%"enrolls in any of these classes"
  courses = models.ManyToManyField('course.Course',blank=True,limit_choices_to={ "active": True },help_text=_ht)
  _ht = _help_template%"RSVPs for any of these events"
  events = models.ManyToManyField('event.Event',blank=True,limit_choices_to={ "allow_rsvp":True },help_text=_ht)
  _ht = "Completing any of these documents will grant this criteria to the user."
  documents = models.ManyToManyField('redtape.Document',blank=True)
  __unicode__ = lambda self: self.name
  def user_can_grant(self,user):
    if user.is_toolmaster:
      return True
    for course in self.courses.all():
      if course.session_set.filter(user=user):
        return True
  @property
  def as_json(self):
    course_fields = ['id','name']
    courses_json = [{f:getattr(c,f) for f in course_fields} for c in self.courses.all()]
    return {
      'id': self.id,
      'name': self.name,
      'course_ids': list(self.courses.all().values_list('id',flat=True)),
      'courses': courses_json
    }
  class Meta:
    ordering = ('name',)

class ActiveUserCriterionManager(models.Manager):
  def get_queryset(self):
    _q = models.Q(expires__isnull=True)|models.Q(expires__gt=datetime.datetime.now())
    return super(ActiveUserCriterionManager,self).get_queryset().filter(_q)

class UserCriterion(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  criterion = models.ForeignKey(Criterion)
  created = models.DateTimeField(auto_now_add=True)
  expires = models.DateTimeField(null=True,blank=True)
  content_type = models.ForeignKey("contenttypes.ContentType")
  object_id = models.IntegerField()
  content_object = GenericForeignKey('content_type', 'object_id')
  active_objects = ActiveUserCriterionManager()
  objects = models.Manager()
  def set_next_expiration(self):
    #! TODO eventually this shoul set the experation based off the content object
    #! eg, if the content object is a signature, the signature could have an expiration
    #! for now this just kills expiration
    self.expires = None
  __unicode__ = lambda self: "%s for %s"%(self.user,self.criterion)

class CriterionModel(models.Model):
  """A model that will generate a user criterion upon completion"""
  datetime = models.DateTimeField(default=datetime.datetime.now)
  completed = models.DateTimeField(null=True,blank=True)
  failed = models.DateTimeField(null=True,blank=True)
  automatic = False # If true criterion will be granted without completion
  as_json = property(lambda self: {a:getattr(self,a) for a in self.json_fields})
  json_fields = ['user_id','username','completed','display_name','id','failed']
  username = property(lambda self: self.user.username)
  display_name = property(lambda self: unicode(self))
  def save(self,*args,**kwargs):
    if self.automatic:
      self.completed = datetime.datetime.now()
    super(CriterionModel,self).save(*args,**kwargs)
    if self.user and self.completed:
      for criterion in self.get_criteria():
        defaults = {'content_object':self}
        try:
          u,new = UserCriterion.active_objects.get_or_create(user=self.user,criterion=criterion,defaults=defaults)
        except UserCriterion.MultipleObjectsReturned:
          print 'deleting for ',self
          UserCriterion.active_objects.filter(user=self.user,criterion=criterion).delete()
          u,new = UserCriterion.active_objects.get_or_create(user=self.user,criterion=criterion,defaults=defaults)
        u.content_object = self
        u.expires = u.set_next_expiration()
        u.save()
    else:
      ct = ContentType.objects.get_for_model(self)
      UserCriterion.active_objects.filter(content_type=ct,object_id=self.id).delete()
  def has_completed_permission(self,user):
    return user.is_superuser or user.is_toolmaster
  def get_criteria(self):
    raise NotImplementedError("%s does not define a 'get_criteria' model"%self.__class__)
  class Meta:
    abstract = True

class Group(models.Model):
  name = models.CharField(max_length=32)
  color = RGBColorField()
  column = models.IntegerField(choices=[(0,"left"),(1,"right")])
  row = models.IntegerField()
  @property
  def as_json(self):
    return {key:getattr(self,key) for key in ['id','name','color','row','column']}
  __unicode__ = lambda self: self.name
  class Meta:
    ordering = ('name',)

class DoorGroup(models.Model):
  name = models.CharField(max_length=32)
  _ht = "List all the doors this can open."
  description = models.TextField(help_text=_ht)
  __unicode__ = lambda self: self.name
  class Meta:
    ordering = ('id',)

class Permission(models.Model):
  name = models.CharField(max_length=32)
  abbreviation = models.CharField(max_length=16,help_text="For badge.")
  room = models.ForeignKey('geo.Room')
  group = models.ForeignKey(Group,null=True,blank=True)
  _ht = "Requires all these criteria to access these tools."
  criteria = models.ManyToManyField(Criterion,blank=True,help_text=_ht)
  order = models.IntegerField(default=999)
  __unicode__ = lambda self: self.name
  tools_json = property(lambda self: [t.as_json for t in self.tool_set.all()])
  criteria_json = property(lambda self: [c.as_json for c in self.criteria.all()])
  @property
  def as_json(self):
    return {
      'id': self.id,
      'name': self.name,
      'abbreviation': self.abbreviation,
      'room_id': self.room_id,
      'tool_ids': list(self.tool_set.all().values_list('id',flat=True)),
      'criterion_ids': list(self.criteria.all().values_list('id',flat=True)),
      'criteria_json': self.criteria_json,
      'group_id': self.group_id,
      'tools_json': self.tools_json
    }
  def check_for_user(self,user):
    return all([UserCriterion.objects.filter(user=user,criterion=c).count() for c in self.criteria.all()])
  def get_all_user_ids(self,fieldname='user_id'):
    groups = []
    for criterion in self.criteria.all():
      groups.append(set(criterion.usercriterion_set.all().values_list(fieldname,flat=True)))
    return set.union(*groups)
  def get_grantable_criteria(self,user):
    return [c for c in self.criteria.all() if c.user_can_grant(user)]
  class Meta:
    ordering = ('group','order')

class Holiday(models.Model):
  name = models.CharField(blank=True,max_length=32)
  date = models.DateField()
  __unicode__ = lambda self: "%s (%s)"%(self.name or "unnamed",self.date)
  class Meta:
    ordering = ("-date",)

class Schedule(models.Model):
  name = models.CharField(max_length=32)
  __unicode__ = lambda self: self.name
  as_json = property(lambda self: {d.dow: [d.start,d.end] for d in self.scheduleday_set.all()})
  def save(self,*args,**kwargs):
    super(Schedule,self).save(*args,**kwargs)
    if not self.scheduleday_set.count():
      for i,d in DOW_CHOICES:
        ScheduleDay.objects.create(schedule=self,dow=i)

DOW_CHOICES = zip(range(7),['Su','Mo','Tu','We','Th','Fr','Sa'])

class ScheduleDay(models.Model):
  schedule = models.ForeignKey(Schedule)
  dow = models.IntegerField(choices=DOW_CHOICES)
  start = models.CharField(max_length=4,default="1000")
  end = models.CharField(max_length=4,default="2200")
  __unicode__ = lambda self: "%s: %s-%s"%(self.get_dow_display(),self.start,self.end)
  class Meta:
    ordering = ('dow',)

class PermissionSchedule(models.Model):
  permission = models.ForeignKey(Permission)
  schedule = models.ForeignKey(Schedule)
  levels = models.ManyToManyField('membership.Level')

def reset_tools_json(context="no context provided"):
  values = {
    'permissions_json': json.dumps([p.as_json for p in Permission.objects.all()]),
    'groups_json': json.dumps([g.as_json for g in Group.objects.all().order_by("row","column")]),
    'criteria_json': json.dumps([c.as_json for c in Criterion.objects.all()])
  }
  text = render_to_string('tool/tools.json',values)
  f = open(os.path.join(settings.STATIC_ROOT,'_tools.json'),'w')
  f.write(text)
  f.close()
  os.rename(os.path.join(settings.STATIC_ROOT,'_tools.json'),os.path.join(settings.STATIC_ROOT,'tools.json'))

  dt = datetime.datetime.now()

def new_key():
  return "".join([random.choice(string.letters+string.digits) for i in range(30)])

class APIKey(models.Model):
  key = models.CharField(max_length=30,default=new_key)
  __unicode__ = lambda self: self.key

class CheckoutItem(models.Model):
  name = models.CharField(max_length=64)
  _ht = 'Only rooms marked "has checkoutitems" appear here'
  room = models.ForeignKey("geo.Room",limit_choices_to={'has_checkoutitems': True},help_text=_ht)
  __unicode__ = lambda self: self.name
  class Meta:
    ordering = ('name',)

class ToolCheckoutItemGroup(models.Model):
  name = models.CharField(max_length=64)
  tools = models.ManyToManyField(Tool)
  checkoutitems = models.ManyToManyField(CheckoutItem)
  __unicode__ = lambda self: self.name
  class Meta:
    ordering = ('name',)
