from django.conf import settings
from django.contrib import admin

from .models import Person, Subject, Message, SubjectFAQ, FAQ

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
  pass

class SubjectFAQInline(admin.TabularInline):
  model = SubjectFAQ
  extra = 0

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
  list_display = ('__str__','order','_message_count')
  list_editable = ('order',)
  inlines = [SubjectFAQInline]
  _message_count = lambda self,obj: obj.message_set.count()

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
  list_filter = ('subject',)
  list_display = ("_display","__str__","datetime")
  list_display_links = ("__str__",)
  readonly_fields = ("read_count",)
  def _display(self,obj):
    _s = "%sadmin/img/icon-%s.gif"%(settings.STATIC_URL,"yes" if obj.marked_read else "no")
    _c = " +%s"%obj.read_count if obj.read_count else ""
    return "<img src='%s'>%s"%(_s,_c)
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
  pass

