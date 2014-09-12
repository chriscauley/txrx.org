from django.template import Library

from course.models import Course
from event.utils import get_room_conflicts as _get_room_conflicts

register = Library()

@register.simple_tag(takes_context=True)
def get_room_conflicts(context):
  user = context['request'].user
  if not (user.is_superuser or user.group_set.filter(name="Event Coordinator")):
    return ''
  context['room_conflicts'] = _get_room_conflicts()
  return ''
