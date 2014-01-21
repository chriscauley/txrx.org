import os, re, uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template.defaultfilters import slugify
from django.utils.hashcompat import md5_constructor
from django.utils.http import urlquote

from crop_override import CropOverride, OriginalImage
from timezones.fields import TimeZoneField
import tagging

from db.models import SlugModel, OrderedModel, UserModel
from codrspace.managers import SettingManager
from .templatetags.short_codes import explosivo
from instagram.models import InstagramPhoto
from txrx.utils import cached_method, cached_property

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
  description = property(lambda self: explosivo(self.content))

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

  list_users = property(lambda self: [self.author])

  @models.permalink
  def get_absolute_url(self):
    return ("post_detail", [self.author.username, self.slug])

tagging.register(Post)

class FileModel(models.Model):
  """An abstract file model. Needs a file field which will be a models.FileField"""
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

class MiscFile(FileModel):
  file = models.FileField(upload_to='uploads/file/%Y-%m')

SOURCE_CHOICES = (
  ('web','Web'),
  ('instagram','Instagram'),
  ('twittpic','TwittPic'),
  ('email','Email'),
  ('misc','Miscelaneous'),
  )

class Photo(FileModel):
  file = OriginalImage("Photo",upload_to='uploads/photos/%Y-%m', null=True,max_length=200)
  caption = models.TextField(null=True,blank=True)
  instagramphoto = models.ForeignKey(InstagramPhoto,null=True,blank=True)
  approved = models.BooleanField(default=False)
  source = models.CharField(choices=SOURCE_CHOICES,default="web",max_length=16)
  kwargs = dict(upload_to='uploads/photos/%Y-%m', original='file')
  _sh = "Usages: Blog Photo, Tool Photo"
  square_crop = CropOverride('Square Crop (1:1)', aspect='1x1',help_text=_sh,**kwargs)
  _lh = "Usages: Featured Blog Photo, Lab Photo"
  landscape_crop = CropOverride('Landscape Crop (5:3)', aspect='5x3',help_text=_lh,**kwargs)
  _ph = "Usages: None"
  portrait_crop = CropOverride('Portrait Crop (3:5)', aspect='3x5',help_text=_ph,**kwargs)

class PhotoSetManager(models.Manager):
  def live(self,*args,**kwargs):
    return self.filter(*args,**kwargs).filter(active=True,setphotos__isnull=False).distinct()

class PhotoSet(SlugModel,UserModel):
  setphotos = models.ManyToManyField(Photo,through="SetPhoto")
  _ht = "If true, this photoset will appear on the photoset index page"
  active = models.BooleanField(default=False,help_text=_ht)
  objects = PhotoSetManager()
  def get_photos(self):
    return self.setphotos.filter(approved=True)
  first_photo = property(lambda self: self.get_photos()[0])
  get_absolute_url = lambda self: reverse('photoset_detail',args=[self.id,unicode(self)])

class SetPhoto(OrderedModel):
  photo = models.ForeignKey(Photo,null=True,blank=True)
  photoset = models.ForeignKey(PhotoSet)
  def get_photo(self):
    return self.photo
  def __unicode__(self):
    return unicode(self.get_photo())

class TaggedPhoto(models.Model):
  photo = models.ForeignKey(Photo)
  content_type = models.ForeignKey("contenttypes.ContentType")
  object_id = models.IntegerField()
  content_object = generic.GenericForeignKey('content_type', 'object_id')
  order = models.IntegerField(default=9999)

class PhotoSetConnection(models.Model):
  photoset = models.ForeignKey(PhotoSet)
  content_type = models.ForeignKey("contenttypes.ContentType")
  object_id = models.IntegerField()
  content_object = generic.GenericForeignKey('content_type', 'object_id')
  class Meta:
    unique_together = ('content_type','object_id')
  __unicode__ = lambda self: "conection: %s %s"%(self.content_type,self.object_id)

class PhotosMixin():
  @cached_property
  def _ct_id(self):
    return ContentType.objects.get_for_model(self.__class__).id
  @cached_method
  def get_photos(self):
    return list(Photo.objects.filter(taggedphoto__content_type_id=self._ct_id,
                                     taggedphoto__object_id=self.id))

class SetModel():
  """ A model that has a PhotoSetConnection attached to it. """
  photoset = None
  _photoset_checked = False
  def get_photoset(self):
    if self._photoset_checked:
      return self.photoset
    self._photoset_checked = True
    try:
      content_type = ContentType.objects.get_for_model(self.__class__)
      self.photoset = PhotoSet.objects.get(
        photosetconnection__content_type=content_type,
        photosetconnection__object_id=self.id)
    except PhotoSet.DoesNotExist:
      pass
    return self.photoset
  def get_or_create_photoset(self):
    if self.get_photoset():
      return self.get_photoset()
    photoset = PhotoSet(
      title="Photos for %s"%str(self),
      user_id=getattr(self,'user_id',1)
      )
    photoset.save()
    content_type = ContentType.objects.get_for_model(self.__class__)
    PhotoSetConnection(content_type=content_type,photoset=photoset,object_id=self.id).save()
    self._photoset_checked = True
    self.photoset = photoset
    return photoset

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
