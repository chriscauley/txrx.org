from django.contrib import admin

from .models import Document, Signature, DocumentField

from jsignature.utils import draw_signature
import base64
import cStringIO

import json

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
  list_display = ("__unicode__","signature_required","login_required")

@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
  readonly_fields = ('datetime','document','date_typed','name_typed','user','_data')
  exclude = ('completed','data')
  def _data(self,obj):
    fields = obj.get_fields()
    rows = "".join(["<tr><th>{name}</th><td>{value}</td></tr>".format(**f) for f in fields])
    return "<table class='table'>%s</table>"%rows
  _data.allow_tags = True
