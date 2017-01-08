from django.contrib import admin

from .models import Document, Signature, DocumentField, Service

import base64
import cStringIO

import json
from lablackey.utils import latin1_to_ascii

class DocumentFieldInline(admin.TabularInline):
  model = DocumentField
  extra = 0
  exclude = ("data","slug")

@admin.register(DocumentField)
class DocumentFieldAdmin(admin.ModelAdmin):
  readonly_fields = ("_data",)
  def _data(self,obj):
    return "<pre>%s</pre>"%json.dumps(obj.data,indent=4)
  _data.allow_tags = True

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
  inlines = [DocumentFieldInline]
  list_display = ("__unicode__","login_required")

@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
  readonly_fields = ('datetime','document','user','_data')
  exclude = ('completed','data')
  search_fields = ("user__username",)
  list_display = ("__unicode__","_data")
  list_filter = ("document",)
  def _data(self,obj):
    if not obj.data:
      return
    fields = obj.get_fields()
    for field in fields:
      field['value'] = latin1_to_ascii(field['value'])
    try:
      rows = "".join(["<tr><th>{name}</th><td>{value}</td></tr>".format(**f) for f in fields])
      return "<table class='table'>%s</table>"%rows
    except:
      return "unicode error"
  _data.allow_tags = True

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
  list_display = ("__unicode__","price","member_price")
  list_editable = ("price","member_price")
