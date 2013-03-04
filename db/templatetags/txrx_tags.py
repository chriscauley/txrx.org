from django import template

register = template.Library()

@register.filter(name='noemail')
def noemail(value):
  """Google groups style email obfuscation."""
  if not '@' in value:
    return value
  a,b = value.split('@')
  return '%s...@%s'%(a[:len(a)/2],b)
