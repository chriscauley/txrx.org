from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

from lablackey.utils import cached_method, cached_property

from crop_override import CropOverride, OriginalImage
from sorl.thumbnail import get_thumbnail
import os

class FileModel(models.Model):
  """An abstract file model. Needs a file field which will be a models.FileField"""
  filename = models.CharField(max_length=200,editable=False)
  name = models.CharField(null=True,blank=True,max_length=500)
  user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True)
  upload_dt = models.DateTimeField(auto_now_add=True)
  __unicode__ = lambda self: self.name or self.filename

  def type(self):
    ext = os.path.splitext(self.filename)[1].lower()
    # map file-type to extension
    types = {
      'image': ('.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff','.bmp',),
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
  ('twittpic','TwittPic'),
  ('email','Email'),
  ('misc','Miscelaneous'),
  )

EXTERNAL_TYPE_CHOICES = (
  ('gfycat','Gfycat'),
  ('vortex','Curly Vortex')
)

class PhotoTag(models.Model):
  name = models.CharField(max_length=32)
  __unicode__ = lambda self: self.name
  class Meta:
    ordering = ('-name',)

class Photo(FileModel):
  file = OriginalImage("Photo",upload_to='uploads/photos/%Y-%m', null=True,max_length=200)
  caption = models.TextField(null=True,blank=True)
  approved = models.BooleanField(default=False)
  source = models.CharField(choices=SOURCE_CHOICES,default="web",max_length=16)
  tags = models.ManyToManyField(PhotoTag,blank=True)
  kwargs = dict(upload_to='uploads/photos/%Y-%m', original='file',max_length=200)
  _sh = "Usages: Blog Photo, Tool Photo"
  square_crop = CropOverride('Square Crop (1:1)', aspect='1x1',help_text=_sh,**kwargs)
  _lh = "Usages: Featured Blog Photo, Lab Photo"
  landscape_crop = CropOverride('Landscape Crop (3:2)', aspect='3x2',help_text=_lh,**kwargs)
  _ph = "Usages: None"
  portrait_crop = CropOverride('Portrait Crop (2:3)', aspect='2x3',help_text=_ph,**kwargs)
  external_url = models.URLField(null=True,blank=True)
  thumbnail_url = property(lambda self: get_thumbnail(self.file,"200x200",crop="center").url)
  @property
  def as_json(self):
    return {
      'id': self.id,
      'name': self.name,
      'thumbnail': self.thumbnail_url,
    }
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
  content_object = GenericForeignKey('content_type', 'object_id')
  order = models.IntegerField(default=9999)

class PhotosMixin(object):
  @cached_property
  def first_photo(self):
    try:
      return self.get_photos()[0]
    except IndexError:
      return Photo.objects.get(id=144)
  @cached_property
  def _ct_id(self):
    return ContentType.objects.get_for_model(self.__class__).id
  @cached_method
  def get_photos(self):
    if getattr(self,"_use_default_photo",False):
      return self._get_photos() or [Photo.objects.get(id=144)]
    return self._get_photos()
  def _get_photos(self):
    return list(Photo.objects.filter(taggedphoto__content_type_id=self._ct_id,
                                     taggedphoto__object_id=self.id).order_by("taggedphoto__order"))

class FilesMixin(object):
  @cached_property
  def first_file(self):
    try:
      return self.get_files()[0]
    except IndexError:
      return MiscFile.objects.get(id=144)
  @cached_property
  def _ct_id(self):
    return ContentType.objects.get_for_model(self.__class__).id
  @cached_method
  def get_files(self):
    return self._get_files()
  def _get_files(self):
    return list(MiscFile.objects.filter(
      taggedfile__content_type_id=self._ct_id,
      taggedfile__object_id=self.id,
      taggedfile__private=False
    ).order_by("taggedfile__order"))
  @cached_method
  def get_private_files(self):
    return self._get_private_files()
  def _get_private_files(self):
    return list(MiscFile.objects.filter(
      taggedfile__content_type_id=self._ct_id,
      taggedfile__object_id=self.id,
      taggedfile__private=True
    ).order_by("taggedfile__order"))
  class Meta:
    abstract = True


class TaggedFile(models.Model):
  file = models.ForeignKey(MiscFile)
  content_type = models.ForeignKey("contenttypes.ContentType")
  object_id = models.IntegerField()
  content_object = GenericForeignKey('content_type', 'object_id')
  order = models.IntegerField(default=9999)
  _ht = "Files will not appear until after the user has completed a class."
  private = models.BooleanField(default=False,help_text=_ht)
