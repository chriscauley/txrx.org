from django.template import Library

from course.models import Course, Session
from event.utils import get_room_conflicts, get_person_conflicts
from membership.models import Subscription

import datetime

register = Library()

@register.filter
def is_event_coordinator(user):
  return user.is_superuser or user.groups.filter(name="Event Coordinator")

@register.filter
def is_course_manager(user):
  return user.is_superuser or user.groups.filter(name="Course Manager")

@register.simple_tag(takes_context=True)
def get_conflicts(context):
  context['room_conflicts'] = get_room_conflicts()
  context['person_conflicts'] = get_person_conflicts()
  return ''

@register.simple_tag(takes_context=True)
def get_courses_needed(context):
  #disabling next line because we're not using it
  #context['courses_needed'] = Course.objects.courses_needed()
  context['inactive_sessions'] = Session.objects.filter(active=False)
  return ''

@register.simple_tag(takes_context=True)
def get_pastdue_subscriptions(context):
  twodays = datetime.datetime.now()-datetime.timedelta(2)
  subscriptions = Subscription.objects.filter(canceled__isnull=True,paid_until__lte=twodays)
  context['pastdue_subscriptions'] = subscriptions.order_by("-paid_until")
  return ''

@register.simple_tag(takes_context=True)
def get_overbooked_sessions(context):
  sessions = Session.objects.filter(last_date__gte=datetime.datetime.now())
  sessions = [s for s in sessions if s.full and s.total_students > s.overbook + s.course.max_students]
  context['overbooked_sessions'] = sessions
  return ''
