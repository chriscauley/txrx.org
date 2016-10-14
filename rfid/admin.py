from django.contrib import admin

from .models import RFIDLog

@admin.register(RFIDLog)
class RFIDLogAdmin(admin.ModelAdmin):
  readonly_fields = ('rfid_number','data','user')
