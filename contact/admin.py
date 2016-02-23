from django.conf import settings
from django.contrib import admin

from .models import Person, Subject, Message, SubjectFAQ, FAQ

class PersonAdmin(admin.ModelAdmin):
  pass

class SubjectFAQInline(admin.TabularInline):
  model = SubjectFAQ
  extra = 0

class SubjectAdmin(admin.ModelAdmin):
  list_display = ('__unicode__','order','_message_count')
  list_editable = ('order',)
  inlines = [SubjectFAQInline]
  _message_count = lambda self,obj: obj.message_set.count()

class MessageAdmin(admin.ModelAdmin):
  list_filter = ('subject',)
  list_display = ("_display","__unicode__","datetime")
  list_display_links = ("__unicode__",)
  readonly_fields = ("read_count",)
  def _display(self,obj):
    _s = "%sadmin/img/icon-%s.gif"%(settings.STATIC_URL,"yes" if obj.marked_read else "no")
    _c = " +%s"%obj.read_count if obj.read_count else ""
    return "<img src='%s'>%s"%(_s,_c)
  _display.allow_tags = True
class FAQAdmin(admin.ModelAdmin):
  pass

admin.site.register(Person, PersonAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(FAQ, FAQAdmin)
