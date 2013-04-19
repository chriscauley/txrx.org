import os
import re
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.hashcompat import md5_constructor
from django.core.cache import cache
from django.utils.http import urlquote
from django.conf import settings

from crop_override import CropOverride, OriginalImage
from timezones.fields import TimeZoneField
from tastypie.models import create_api_key
import tagging

from db.models import SlugModel, OrderedModel, UserModel
from codrspace.managers import SettingManager
from instagram.models import InstagramPhoto

models.signals.post_save.connect(create_api_key, sender=User)

try:
  from south.modelsinspector import add_introspection_rules
  add_introspection_rules([], ["^timezones\.fields\.TimeZoneField"])
except ImportError:
  #necessary if you're going to use south
  pass

def invalidate_cache_key(fragment_name, *variables):
  args = md5_constructor(u':'.join([urlquote(var) for var in variables]))
  cache_key = 'template.cache.%s.%s' % (fragment_name, args.hexdigest())
  cache.delete(cache_key)


class Post(models.Model):

  STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
  )

  title = models.CharField(max_length=200, blank=True)
  content = models.TextField(blank=True)
  slug = models.SlugField(max_length=75)
  author = models.ForeignKey(User)
  status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=0)
  publish_dt = models.DateTimeField("Publish On",null=True)
  create_dt = models.DateTimeField(auto_now_add=True)
  update_dt = models.DateTimeField(auto_now=True)
  _h = "Featured blogs must have a photo or they won't appear at all."
  featured = models.BooleanField(default=False,help_text=_h)
  photo = models.ForeignKey("Photo",null=True,blank=True)

  class Meta:
    unique_together = ("slug", "author")
    ordering = ('-featured','-publish_dt',)
  __unicode__ = lambda self: self.title or 'Untitled'

  def url(self):
    return '%s%s' % (settings.SITE_URL, self.get_absolute_url(),)

  def save(self, *args, **kwargs):
    super(Post, self).save(*args, **kwargs)

    # Invalidate cache for all individual posts and the list of posts
    invalidate_cache_key('content', self.pk)

  @models.permalink
  def get_absolute_url(self):
    return ("post_detail", [self.author.username, self.slug])

tagging.register(Post)

class FileModel(models.Model):
  """An abstract file model. Needs a file model which will be a models.FileField"""
  filename = models.CharField(max_length=200,editable=False)
  name = models.CharField(null=True,blank=True,max_length=500)
  user = models.ForeignKey(User,null=True,blank=True)
  upload_dt = models.DateTimeField(auto_now_add=True)
  __unicode__ = lambda self: self.name or self.filename

  def type(self):
    ext = os.path.splitext(self.filename)[1].lower()
    # map file-type to extension
    types = {
      'image': ('.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff',
            '.bmp',),
      'text': ('.txt', '.doc', '.docx'),
      'spreadsheet': ('.csv', '.xls', '.xlsx'),
      'powerpoint': ('.ppt', '.pptx'),
      'pdf': ('.pdf'),
      'video': ('.wmv', '.mov', '.mpg', '.mp4', '.m4v'),
      'zip': ('.zip'),
      'code': ('.txt', '.py', '.htm', '.html', '.css', '.js', '.rb', '.sh'),
    }

    for type in types:
      if ext in types[type]:
        return type
    return 'code'

  def shortcode(self):
    shortcode = ''
    if self.type() == 'image':
      shortcode = "![%s](%s)" % (self.filename, self.file.url)
    if self.type() == 'code':
      shortcode = "[local %s]" % self.file.name
    return shortcode

  def save(self,*args,**kwargs):
    self.filename = self.filename or str(self.file).split('/')[-1]
    self.name = self.name or self.filename
    super(FileModel,self).save(*args,**kwargs)

  class Meta:
    abstract = True

class Photo(FileModel):
  file = OriginalImage("Photo",upload_to='uploads/photos/%Y-%m', null=True)
  caption = models.TextField(null=True,blank=True)
  instagramphoto = models.ForeignKey(InstagramPhoto,null=True,blank=True)
  kwargs = dict(upload_to='uploads/photos/%Y-%m', original='file')
  _sh = "Usages: Blog Photo, Tool Photo"
  square_crop = CropOverride('Square Crop (1:1)', aspect='1x1',help_text=_sh,**kwargs)
  _lh = "Usages: Featured Blog Photo, Lab Photo"
  landscape_crop = CropOverride('Landscape Crop (5:3)', aspect='5x3',help_text=_lh,**kwargs)
  _ph = "Usages: None"
  portrait_crop = CropOverride('Portrait Crop (3:5)', aspect='3x5',help_text=_ph,**kwargs)

class PhotoSet(SlugModel,UserModel):
  setphotos = models.ManyToManyField(Photo,through="SetPhoto")
  def get_photos(self):
    return [p.get_photo() for p in self.setphoto_set.all()]

class SetPhoto(OrderedModel):
  photo = models.ForeignKey(Photo,null=True,blank=True)
  photoset = models.ForeignKey(PhotoSet)
  def get_photo(self):
    return self.photo
  def __unicode__(self):
    return unicode(self.get_photo())

class Setting(models.Model):
  """
  Settings model for specific blog settings
  """
  blog_title = models.CharField(max_length=75, null=True, blank=True)
  blog_tagline = models.CharField(max_length=150, null=True, blank=True)
  name = models.CharField(max_length=30, null=True, blank=True)
  bio = models.TextField(null=True, blank=True)
  user = models.ForeignKey(User, editable=False)
  timezone = TimeZoneField(default="US/Central")

  objects = SettingManager()


class Profile(models.Model):
  git_access_token = models.CharField(max_length=75, null=True)
  user = models.OneToOneField(User)
  meta = models.TextField(null=True)

  def get_meta(self):
    from django.utils import simplejson
    if self.meta:
      return simplejson.loads(self.meta)
    return ''
