from django.contrib import admin

from .models import Document, Signature, DocumentField

class DocumentFieldInline(admin.TabularInline):
  model = DocumentField
  extra = 0

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
  inlines = [DocumentFieldInline]

@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
  readonly_fields = ('datetime','document','date_typed','name_typed','user','_signature','_data')
  exclude = ('completed','data','signature')
  def _signature(self,obj):
    if not obj.signature:
      return
    return "<img src='%s'>"%obj.signature.url
  _signature.allow_tags = True
  def _data(self,obj):
    fields = obj.get_fields()
    rows = "".join(["<tr><th>{name}</th><td>{value}</td></tr>".format(**f) for f in fields])
    return "<table class='table'>%s</table>"%rows
  _data.allow_tags = True
