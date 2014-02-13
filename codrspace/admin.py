from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from crop_override.admin import CropAdmin
from sorl.thumbnail import get_thumbnail

from db.admin import SlugModelAdmin, OrderedModelAdmin, OrderedModelInline
from db.forms import StaffMemberForm

from .models import Post, Photo, SetPhoto, PhotoSet, PhotoSetConnection, MiscFile, TaggedPhoto, PressItem, Banner

class PostAdmin(admin.ModelAdmin):
  list_display = ('__unicode__','user','featured','publish_dt','status')
  list_editable = ('featured','status')
  search_fields = ('content',)

class PhotoAdmin(CropAdmin):
  form = StaffMemberForm
  list_display = ('__unicode__','_thumbnail','approved','upload_dt')
  list_sortable = ('__unicode__','upload_dt')
  list_editable = ('approved',)
  list_filter = ('upload_dt',)
  raw_id_fields = ('user',)
  fieldsets = (
    (None,{'fields': ('name','file',('user','source'),'caption')}),
    ('crops',{'fields': (('square_crop','landscape_crop'),'portrait_crop')}),
    )
  def _thumbnail(self,obj):
    im = get_thumbnail(obj.file,'100x100',crop='center')
    out = '<img src="%s" width="%s" height="%s" />'%(im.url,im.width,im.height)
    return out
  _thumbnail.allow_tags=True

class SetPhotoInline(OrderedModelInline):
  raw_id_fields = ('photo',)
  model = SetPhoto
  extra = 0

class PhotoSetConnectionInline(GenericTabularInline):
  max_num = 1
  model = PhotoSetConnection
  raw_id_fields = ('photoset',)

class TaggedPhotoInline(GenericTabularInline):
  model = TaggedPhoto
  raw_id_fields = ('photo',)
  extra = 0

class PhotoSetAdmin(SlugModelAdmin):
  inlines = [SetPhotoInline] #,PhotoSetConnectionInline]
  list_display = ('__unicode__','active','photo_count')
  list_editable = ('active',)
  raw_id_fields = ('user',)
  def photo_count(self,obj):
    return len(obj.get_photos())
  photo_count.allow_tags = True

admin.site.register(Post,PostAdmin)
admin.site.register(Photo,PhotoAdmin)
admin.site.register(SetPhoto,OrderedModelAdmin)
admin.site.register(PhotoSet,PhotoSetAdmin)
admin.site.register(MiscFile)
admin.site.register(PressItem)
admin.site.register(Banner)
