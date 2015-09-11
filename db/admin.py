from django import forms
from django.contrib import admin
from django.contrib.admin.sites import site
from django.contrib.admin.widgets import ManyToManyRawIdWidget, ForeignKeyRawIdWidget
from django.core.urlresolvers import reverse
from django.db import models
from django.forms.widgets import HiddenInput
from django.utils.encoding import smart_unicode
from django.utils.html import escape

class VerboseForeignKeyRawIdWidget(ForeignKeyRawIdWidget):
  def label_for_value(self, value):
    key = self.rel.get_related_field().name
    try:
      obj = self.rel.to._default_manager.using(self.db).get(**{key: value})
      change_url = reverse(
        "admin:%s_%s_change" % (obj._meta.app_label, obj._meta.object_name.lower()),
        args=(obj.pk,)
      )
      return '&nbsp;<strong><a href="%s">%s</a></strong>' % (change_url, escape(obj))
    except (ValueError, self.rel.to.DoesNotExist):
      return '???'

class VerboseManyToManyRawIdWidget(ManyToManyRawIdWidget):
  def label_for_value(self, value):
    values = value.split(',')
    str_values = []
    key = self.rel.get_related_field().name
    for v in values:
      try:
        obj = self.rel.to._default_manager.using(self.db).get(**{key: v})
        x = smart_unicode(obj)
        change_url = reverse(
          "admin:%s_%s_change" % (obj._meta.app_label, obj._meta.object_name.lower()),
          args=(obj.pk,)
        )
        str_values += ['<strong><a href="%s">%s</a></strong>' % (change_url, escape(x))]
      except self.rel.to.DoesNotExist:
        str_values += [u'???']
    return u', '.join(str_values)

class RawMixin(object):
  def formfield_for_dbfield(self, db_field, **kwargs):
    if db_field.name in self.raw_id_fields:
      kwargs.pop("request", None)
      type = db_field.rel.__class__.__name__
      if type == "ManyToOneRel":
        kwargs['widget'] = VerboseForeignKeyRawIdWidget(db_field.rel, site)
      elif type == "ManyToManyRel":
        kwargs['widget'] = VerboseManyToManyRawIdWidget(db_field.rel, site)
      return db_field.formfield(**kwargs)
    return super(RawMixin, self).formfield_for_dbfield(db_field, **kwargs)

class OrderedModelAdmin(RawMixin,admin.ModelAdmin):
  exclude = ("order",)
  list_editable = ("order",)
  list_display = ("__unicode__","order")
  readonly_fields = ('order',)

class OrderedModelInline(RawMixin,admin.TabularInline):
  formfield_overrides = {
    models.PositiveIntegerField: {'widget': HiddenInput},
  }
  sortable_field_name = "order"
  extra = 0

class SlugModelAdmin(RawMixin,admin.ModelAdmin):
  exclude = ("slug",)

class SlugModelInline(RawMixin,admin.TabularInline):
  exclude = ("slug",)

class NamedTreeModelAdmin(RawMixin,admin.ModelAdmin):
  exclude = ('order',)

