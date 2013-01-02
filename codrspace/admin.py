from django.contrib import admin
from crop_override.admin import CropAdmin
from sorl.thumbnail import get_thumbnail

from db.forms import StaffMemberForm

from .models import Post, Photo

class PostAdmin(admin.ModelAdmin):
  list_display = ('__unicode__','author','featured','publish_dt','status')
  list_editable = ('featured','status')

class PhotoAdmin(CropAdmin):
  form = StaffMemberForm
  list_display = ('__unicode__','_thumbnail')
  def _thumbnail(self,obj):
    im = get_thumbnail(obj.file,'100x100',crop='center')
    out = '<img src="%s" width="%s" height="%s" />'%(im.url,im.width,im.height)
    return out
  _thumbnail.allow_tags=True

admin.site.register(Post,PostAdmin)
admin.site.register(Photo,PhotoAdmin)
