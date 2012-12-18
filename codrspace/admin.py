from django.contrib import admin

from .models import Post, Media

class PostAdmin(admin.ModelAdmin):
  list_display = ('__unicode__','author','featured','publish_dt')
  list_editable = ('featured',)

admin.site.register(Post,PostAdmin)
admin.site.register(Media)
