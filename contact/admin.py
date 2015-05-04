from django.contrib import admin

from .models import Person, Subject, Message, SubjectFAQ, FAQ

class PersonAdmin(admin.ModelAdmin):
  pass

class SubjectFAQInline(admin.TabularInline):
  model = SubjectFAQ
  extra = 0

class SubjectAdmin(admin.ModelAdmin):
  list_display = ('__unicode__','order')
  list_editable = ('order',)
  inlines = [SubjectFAQInline]

class MessageAdmin(admin.ModelAdmin):
  pass

class FAQAdmin(admin.ModelAdmin):
  pass

admin.site.register(Person, PersonAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(FAQ, FAQAdmin)
