from django import template
from django.forms import CheckboxInput

register = template.Library()

@register.filter(name='noemail')
def noemail(value):
  """Google groups style email obfuscation."""
  if not '@' in value:
    return value
  a,b = value.split('@')
  return '%s...@%s'%(a[:len(a)/2],b)

@register.filter(name='is_checkbox')
def is_checkbox(field):
  return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__
