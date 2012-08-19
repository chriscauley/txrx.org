from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField

from lablackey.utils import cached_method
from lablackey.profile.models import ProfileModel, UserModel
from course.models import Section
from project.models import Project

class MembershipManager(models.Manager):
    def active(self):
        return self.filter(monthly__gt=0)

class Membership(models.Model):
    name = models.CharField(max_length=64)
    notes = models.CharField(max_length=256,null=True,blank=True)
    order = models.IntegerField("Level")
    monthly = models.IntegerField("Monthly")
    yearly = models.IntegerField("Yearly")
    student_rate = models.IntegerField("Student Rate",null=True,blank=True)
    objects = MembershipManager()
    def profiles(self):
        return self.profile_set.all()
    class Meta:
        verbose_name = "Membership Level"
        ordering = ("order",)
    __unicode__ = lambda self: self.name

class Role(models.Model):
    name = models.CharField(max_length=64)

class Feature(models.Model):
    membership = models.ForeignKey(Membership)
    text = models.CharField(max_length=128)
    order = models.IntegerField(default=0)
    class Meta:
        ordering = ("order",)

class ProfileManager(models.Manager):
    def list_instructors(self,**kwargs):
        from course.models import Section
        return set([s.user.profile for s in Section.objects.filter(**kwargs)])

class Profile(ProfileModel):
    membership = models.ForeignKey(Membership,default=1)
    #roles = models.ManyToManyField(Role,null=True,blank=True)
    bio = models.TextField(null=True,blank=True)
    _folder = settings.UPLOAD_DIR+'/avatars/%Y-%m'
    avatar = ImageField(max_length=300,upload_to=_folder,null=True,blank=True)
    src = property(lambda self: self.avatar)
    name = lambda self: self.user.username
    objects = ProfileManager()
    @cached_method
    def get_sections(self):
        return Section.objects.filter(user=self.user)
    @cached_method
    def get_projects(self):
        return Project.objects.filter(author=self.user)

class Survey(models.Model):
    user = models.ForeignKey(User,unique=True)
    reasons = models.TextField(blank=True)
    projects = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    expertise = models.TextField(blank=True)
    questions = models.TextField(blank=True)
