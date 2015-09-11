from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from crop_override.admin import CropAdmin
from sorl.thumbnail import get_thumbnail

from lablackey.db.admin import SlugModelAdmin, OrderedModelAdmin, OrderedModelInline, RawMixin
from lablackey.db.forms import StaffMemberForm

from .models import Post, Banner, PressItem
from .forms import PostForm

class PostAdminForm(PostForm):
  """ Just like post form, but with user """
  class Meta:
    model = Post
    fields = ('user','title','slug','content','short_content','publish_dt','tags','status','photo')

class PostAdmin(RawMixin,admin.ModelAdmin):
  form = PostAdminForm
  list_display = ('__unicode__','user','featured','publish_dt','status')
  list_editable = ('featured','status')
  search_fields = ('content',)
  raw_id_fields = ('photo','user')

admin.site.register(Post,PostAdmin)
admin.site.register(PressItem)
admin.site.register(Banner)
