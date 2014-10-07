from django import template
from django.forms import CheckboxInput, Select

register = template.Library()

@register.filter
def is_checkbox(field):
  return field.field.widget.__class__.__name__ == CheckboxInput.__name__

@register.filter
def is_select(field):
  return field.field.widget.__class__.__name__ == Select.__name__
