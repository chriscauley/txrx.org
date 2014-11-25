from django.contrib import messages
from django.contrib import admin

from .models import BulkEmail, BulkEmailRecipient

class BulkEmailRecipientInline(admin.TabularInline):
  model = BulkEmailRecipient

class BulkEmailAdmin(admin.ModelAdmin):
  inlines = [BulkEmailRecipientInline]
  def save_model(self, request, obj, form, change):
    super(BulkEmailAdmin,self).save_model(request, obj, form, change)
    if obj.send_on_save:
      sent_count = 0
      for ber in obj.bulkemailrecipient_set.all():
        if not ber.sent and ber.file1:
          ber.send()
          sent_count += 1
      if sent_count:
        messages.success(request,"messages sent to %s people"%sent_count)
      else:
        messages.warning(request,"No Messages sent. Try removing 'sent on' value and resave twice.")
      ber.save()

admin.site.register(BulkEmail,BulkEmailAdmin)
