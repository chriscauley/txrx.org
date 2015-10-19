from django.contrib import admin

from .models import Document, Signature

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
  pass

@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
  pass
