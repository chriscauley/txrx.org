from django import template
from django.forms import CheckboxInput, Select
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def is_checkbox(field):
  return field.field.widget.__class__.__name__ == CheckboxInput.__name__

@register.filter
def is_select(field):
  return field.field.widget.__class__.__name__ == Select.__name__

def _ptime(time):
  if time.minute == 0 and time.hour in [0,12]:
    return "midnight" if time.hour == 0 else "noon"
  if time.minute == 0:
    return time.strftime("%I %p").lstrip('0')
  return time.strftime("%I:%M %p").lstrip('0')

@register.filter
def format_classtime(classtime):
  start = classtime.start
  end = classtime.end
  s = start.strftime("%b %e, %%s - %%s (%a)")%(_ptime(start),_ptime(end))
  return s.replace("AM","am").replace("PM","pm")

@register.filter
def format_session_classtimes(session):
  return "|".join([format_classtime(ct) for ct in session.classtime_set.all()])

@register.filter
def get_admin_link(obj):
  try:
    url = reverse("admin:%s_%s_change" % (obj._meta.app_label, obj._meta.model_name), args=(obj.id,))
    return mark_safe('<a class="fa fa-pencil edit" href="%s"></a>'%url)
  except:
    return ""
