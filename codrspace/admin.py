from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from crop_override.admin import CropAdmin
from sorl.thumbnail import get_thumbnail

from db.admin import SlugModelAdmin, OrderedModelAdmin, OrderedModelInline
from db.forms import StaffMemberForm

from .models import Post, Photo, MiscFile, TaggedPhoto, PressItem, Banner, TaggedFile
from .forms import PostForm

class PostAdminForm(PostForm):
  """ Just like post form, but with user """
  class Meta:
    model = Post
    fields = ('user','title','slug','content','short_content','publish_dt','tags','status','photo')

class PostAdmin(admin.ModelAdmin):
  form = PostAdminForm
  list_display = ('__unicode__','user','featured','publish_dt','status')
  list_editable = ('featured','status')
  search_fields = ('content',)
  raw_id_fields = ('photo','user')

class PhotoAdmin(CropAdmin):
  form = StaffMemberForm
  list_display = ('__unicode__','_thumbnail','approved','upload_dt')
  list_sortable = ('__unicode__','upload_dt')
  list_editable = ('approved',)
  list_filter = ('upload_dt',)
  search_fields = ('name',)
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

class TaggedPhotoInline(GenericTabularInline):
  model = TaggedPhoto
  raw_id_fields = ('photo',)
  extra = 0

class TaggedFileInline(GenericTabularInline):
  model = TaggedFile
  raw_id_fields = ('file',)
  extra = 0

admin.site.register(Post,PostAdmin)
admin.site.register(Photo,PhotoAdmin)
admin.site.register(MiscFile)
admin.site.register(PressItem)
admin.site.register(Banner)
