from django.contrib import admin

from .models import Document, Signature, DocumentField

import base64
import cStringIO

import json
from lablackey.utils import latin1_to_ascii

class DocumentFieldInline(admin.TabularInline):
  model = DocumentField
  extra = 0
  exclude = ("choices","slug")

@admin.register(DocumentField)
class DocumentFieldAdmin(admin.ModelAdmin):
  readonly_fields = ("_choices",)
  def _choices(self,obj):
    return "<pre>%s</pre>"%json.dumps(obj.get_optgroups() or obj.get_options(),indent=4)
  _choices.allow_tags = True

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
    fields = [{k: latin1_to_ascii(v) for k,v in f.items()} for f in fields]
    try:
      rows = "".join(["<tr><th>{name}</th><td>{value}</td></tr>".format(**f) for f in fields])
      return "<table class='table'>%s</table>"%rows
    except:
      return "unicode error"
  _data.allow_tags = True
