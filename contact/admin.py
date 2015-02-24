from django.contrib import admin

from .models import ContactPerson, ContactSubject, ContactMessage

class ContactPersonAdmin(admin.ModelAdmin):
  pass

class ContactSubjectAdmin(admin.ModelAdmin):
  list_display = ('__unicode__','order')
  list_editable = ('order',)

class ContactMessageAdmin(admin.ModelAdmin):
  pass

admin.site.register(ContactPerson, ContactPersonAdmin)
admin.site.register(ContactSubject, ContactSubjectAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
