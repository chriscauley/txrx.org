from django.conf import settings
from django.conf.urls import url, patterns
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericTabularInline
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template.response import TemplateResponse

from crop_override.admin import CropAdmin
from sorl.thumbnail import get_thumbnail

from db.forms import StaffMemberForm
from .forms import MultiPhotoUploadForm
from .models import PhotoTag, Photo, MiscFile, TaggedPhoto, TaggedFile

import json

class PhotoAdmin(CropAdmin):
  form = StaffMemberForm
  list_display = ('__unicode__','_thumbnail','approved','upload_dt')
  list_sortable = ('__unicode__','upload_dt')
  list_editable = ('approved',)
  list_filter = ('upload_dt','tags',)
  search_fields = ('name',)
  raw_id_fields = ('user',)
  fieldsets = (
    (None,{'fields': ('name','file',('user','source'),'caption','external_url')}),
    ('crops',{'fields': (('square_crop','landscape_crop'),'portrait_crop')}),
    )
  def _thumbnail(self,obj):
    im = get_thumbnail(obj.file,'100x100',crop='center')
    out = '<img src="%s" width="%s" height="%s" />'%(im.url,im.width,im.height)
    return out
  _thumbnail.allow_tags=True
  def get_urls(self):
    urls = super(PhotoAdmin, self).get_urls()
    upload_urls = patterns(
      '',
      url(r'^bulk/$', self.admin_site.admin_view(self.multi_photo_upload_view), name='photos_admin_upload'),
    )
    return upload_urls + urls
  def multi_photo_upload_view(self, request):
    if request.method == "POST" and request.FILES:
      natural_key = request.POST.get('content_type').split('.')
      content_type = ContentType.objects.get_by_natural_key(*natural_key)
      image_list = []
      name = request.POST.get('name',None) or None
      for f in request.FILES.getlist('file'):
        photo = Photo.objects.create(
          name=name,
          file=f,
          user=request.user
        )
        image_list.append(photo.as_json)
        TaggedPhoto.objects.create(
          photo=photo,
          object_id=request.POST['object_pk'],
          content_type=content_type,
        )
      return HttpResponse(json.dumps(image_list))

    template="admin/multi_photo_upload.html"
    return TemplateResponse(request,template,context)

class TaggedPhotoAdmin(admin.ModelAdmin):
  def get_fields(self,request,obj=None):
    fields = super(TaggedPhotoAdmin,self).get_fields(request,obj)
    if obj and not 'dropphoto' in fields:
      return list(fields) + ['dropphoto']
    return fields
  def get_readonly_fields(self,request,obj=None):
    fields = super(TaggedPhotoAdmin,self).get_readonly_fields(request,obj)
    if obj and not 'dropphoto' in fields:
      return list(fields) + ['dropphoto']
    return fields
  def dropphoto(self,obj=None): # only occurs with obj (See get_fields)
    values = {
      'content_type': self.model._meta.app_label+"."+self.model.__name__.lower(),
      'opts': self.model._meta,
      'photos': json.dumps([p.as_json for p in obj.get_photos()]),
      'obj': obj,
      'STATIC_URL':settings.STATIC_URL
    }
    print values
    return render_to_string('admin/dropphoto.html',values).replace('\n','')
  dropphoto.allow_tags = True

class TaggedPhotoInline(GenericTabularInline):
  model = TaggedPhoto
  raw_id_fields = ('photo',)
  fields = ('order','_thumbnail','photo')
  readonly_fields = ('_thumbnail',)
  extra = 0
  def _thumbnail(self,obj):
    im = get_thumbnail(obj.photo.file,'100x100',crop='center')
    out = '<img src="%s" width="%s" height="%s" />'%(im.url,im.width,im.height)
    return out
  _thumbnail.allow_tags=True


class TaggedFileInline(GenericTabularInline):
  model = TaggedFile
  raw_id_fields = ('file',)
  extra = 0

class PhotoTagAdmin(admin.ModelAdmin):
  list_display = ("__unicode__","bulk_link")
  bulk_link = lambda self, obj: "<a href='/media_files/photo/bulk_tag/%s'>Bulk Tag %s Photos</a>"%(obj.pk,obj)
  bulk_link.allow_tags = True

class MiscFileAdmin(admin.ModelAdmin):
  form = StaffMemberForm

admin.site.register(Photo,PhotoAdmin)
admin.site.register(MiscFile,MiscFileAdmin)
admin.site.register(PhotoTag,PhotoTagAdmin)
