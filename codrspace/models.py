import os, re, uuid, datetime, random
from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template.defaultfilters import slugify, striptags
from django.utils.http import urlquote

from crop_override import CropOverride, OriginalImage
from timezones.fields import TimeZoneField
import tagging

from db.models import SlugModel, OrderedModel, UserModel
from .managers import SettingManager
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

EXTERNAL_TYPE_CHOICES = (
  ('gfycat','Gfycat'),
  ('vortex','Curly Vortex')
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
  landscape_crop = CropOverride('Landscape Crop (3:2)', aspect='3x2',help_text=_lh,**kwargs)
  _ph = "Usages: None"
  portrait_crop = CropOverride('Portrait Crop (2:3)', aspect='2x3',help_text=_ph,**kwargs)
  external_url = models.URLField(null=True,blank=True)
  @property
  def external_type(self):
    for t in ['gfycat','youtube','vortex']:
      if t in self.external_url:
        return t
    return 'video'
  def save(self,*args,**kwargs):
    if self.external_url and not '/embed/' in self.external_url:
      self.external_url = self.external_url.replace('youtu.be','youtube.com')
      self.external_url = self.external_url.replace('youtube.com/','youtube.com/embed/')
      if not "?" in self.external_url:
        self.external_url +="?autoplay=1&rel=0"
    super(Photo,self).save(*args,**kwargs)
  class Meta:
    ordering = ('name',)

class TaggedPhoto(models.Model):
  photo = models.ForeignKey(Photo)
  content_type = models.ForeignKey("contenttypes.ContentType")
  object_id = models.IntegerField()
  content_object = generic.GenericForeignKey('content_type', 'object_id')
  order = models.IntegerField(default=9999)

class PhotosMixin():
  @cached_property
  def first_photo(self):
    try:
      return self.get_photos()[0]
    except IndexError:
      return Photo.objects.get(pk=144)
  @cached_property
  def _ct_id(self):
    return ContentType.objects.get_for_model(self.__class__).id
  @cached_method
  def get_photos(self):
    return self._get_photos()
  def _get_photos(self):
    return list(Photo.objects.filter(taggedphoto__content_type_id=self._ct_id,
                                     taggedphoto__object_id=self.id).order_by("taggedphoto__order"))

class FilesMixin():
  @cached_property
  def first_file(self):
    try:
      return self.get_files()[0]
    except IndexError:
      return MiscFile.objects.get(pk=144)
  @cached_property
  def _ct_id(self):
    return ContentType.objects.get_for_model(self.__class__).id
  @cached_method
  def get_files(self):
    return self._get_files()
  def _get_files(self):
    return list(MiscFile.objects.filter(taggedfile__content_type_id=self._ct_id,
                                     taggedfile__object_id=self.id).order_by("taggedfile__order"))

class TaggedFile(models.Model):
  file = models.ForeignKey(MiscFile)
  content_type = models.ForeignKey("contenttypes.ContentType")
  object_id = models.IntegerField()
  content_object = generic.GenericForeignKey('content_type', 'object_id')
  order = models.IntegerField(default=9999)

from feed.models import FeedItemModel

class Post(FeedItemModel,PhotosMixin):
  feed_item_type = 'blog'
  STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
  )

  title = models.CharField(max_length=200, blank=True)
  content = models.TextField(blank=True)
  short_content = models.TextField(null=True,blank=True)
  get_short_content = lambda self: self.short_content or striptags(explosivo(self.content))
  slug = models.SlugField(max_length=75)
  status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=0)
  publish_dt = models.DateTimeField("Publish On",null=True)
  create_dt = models.DateTimeField(auto_now_add=True)
  update_dt = models.DateTimeField(auto_now=True)
  _h = "Featured blogs must have a photo or they won't appear at all."
  featured = models.BooleanField(default=False,help_text=_h)
  photo = models.ForeignKey("Photo",null=True,blank=True)
  description = property(lambda self: explosivo(self.content))
  objects = models.Manager()

  @cached_property
  def first_photo(self):
    return self.photo or super(Post,self).first_photo

  class Meta:
    unique_together = ("slug", "user")
    ordering = ('-featured','-publish_dt',)
  __unicode__ = lambda self: self.title or 'Untitled'

  def url(self):
    return '%s%s' % (settings.SITE_URL, self.get_absolute_url(),)

  def save(self, *args, **kwargs):
    super(Post, self).save(*args, **kwargs)

  #depracate please
  list_users = property(lambda self: [self.user])

  @models.permalink
  def get_absolute_url(self):
    return ("post_detail", [self.user.username, self.slug])

  """def update_feed(self):
    feed_item = FeedItem.get_for_object(self)
    feed_item.title = self.title
    feed_item.thumbnail = prep_thumbnail(self.photo.file)
    feed_item.publish_dt = self.publish_dt
    feed_item.item_type = 'blog'
    feed_item.user = self.user
    feed_item.save()"""

tagging.register(Post)

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

class PressItem(models.Model):
  title = models.CharField(max_length=64)
  url = models.URLField(max_length=256)
  publish_dt = models.DateField("Date")
  __unicode__ = lambda self: self.title
  class Meta:
    ordering = ('-publish_dt',)

WEIGHT_CHOICES = zip(range(1,6),range(1,6))

class BannerManager(models.Manager):
  def get_random(self,*args,**kwargs):
    today = datetime.date.today()
    banners = self.filter(start_date__lte=today,end_date__gte=today,active=True)
    if not banners:
      return
    choices = []
    for i,banner in enumerate(banners):
      choices += [i]*banner.weight
    return banners[random.choice(choices)]

class Banner(models.Model):
  start_date = models.DateField(default=datetime.date.today)
  end_date = models.DateField(blank=True)
  name = models.CharField(max_length=64)
  header = models.CharField(default="Featured Event",max_length=32)
  active = models.BooleanField(default=True)
  src = models.ImageField(upload_to="banners")
  url = models.CharField(max_length=200)
  weight = models.IntegerField(choices=WEIGHT_CHOICES)
  objects = BannerManager()
  __unicode__ = lambda self: self.name
  def save(self,*args,**kwargs):
    self.end_date = self.end_date or datetime.date(2099,1,1)
    super(Banner,self).save(*args,**kwargs)
  class Meta:
    ordering = ('name',)
