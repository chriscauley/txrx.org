from django.template import Library

from course.models import Course
from event.utils import get_room_conflicts as _get_room_conflicts
from membership.models import Flag

import datetime

register = Library()

@register.filter
def is_event_coordinator(user):
  return user.is_superuser or user.groups.filter(name="Event Coordinator")

@register.filter
def is_course_manager(user):
  return user.is_superuser or user.groups.filter(name="Course Manager")

@register.simple_tag(takes_context=True)
def get_room_conflicts(context):
  context['room_conflicts'] = _get_room_conflicts()
  return ''

@register.simple_tag(takes_context=True)
def get_courses_needed(context):
  context['courses_needed'] = Course.objects.courses_needed()
  return ''
  
@register.simple_tag(takes_context=True)
def get_user_flags(context):
  today, upcoming, pastdue = [], [], []
  now = datetime.datetime.now()
  for flag in Flag.objects.filter(status__in=Flag.ACTION_CHOICES):
    if flag.date_of_next_action > now:
      upcoming.append(flag)
    elif flag.date_of_next_action < now:
      pastdue.append(flag)
    else:
      today.append(flag)
  context['user_flags'] = [
    ['Action Past Due',pastdue,'danger'],
    ['Todays Flags',today,'success'],
    ['Upcoming Flags',upcoming,'']
  ]
  return ''
