from django.contrib import admin

from sms.models import SMSNumber

from lablackey.db.admin import RawMixin

@admin.register(SMSNumber)
class SMSNumberAdmin(RawMixin,admin.ModelAdmin):
  pass
