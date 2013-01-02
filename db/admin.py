from django.contrib import admin
from django.db import models
from django.forms.widgets import HiddenInput

class OrderedModelAdmin(admin.ModelAdmin):
  exclude = ("order",)
  list_editable = ("order",)
  list_display = ("__unicode__","order")
  readonly_fields = ('order',)

class OrderedModelInline(admin.TabularInline):
  formfield_overrides = {
    models.PositiveIntegerField: {'widget': HiddenInput},
    }
  sortable_field_name = "order"
  extra = 0

class SlugModelAdmin(admin.ModelAdmin):
  exclude = ("slug",)

class SlugModelInline(admin.TabularInline):
  exclude = ("slug",)

class ColumnModelAdmin(admin.ModelAdmin):
  list_filter = ('column',)
