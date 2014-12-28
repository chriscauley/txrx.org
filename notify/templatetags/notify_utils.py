from django import template
from django.core.urlresolvers import reverse

from course.models import Evaluation, Enrollment

import datetime

register = template.Library()

@register.filter
def get_notifications(request):
  if not request.user.is_authenticated():
    return []
  out = []
  evaluations = Evaluation.objects.filter(enrollment__session__user=request.user)
  """if evaluations:
    out.append({
      'url': reverse('course:instructor_evaluations',args=[request.user.pk]),
      'link_text': "Course Evaluations",
      'new_count': 0
    })"""
  pending_evaluations = Enrollment.objects.pending_evaluation(user=request.user)
  if pending_evaluations:
    out.append({
      'url': reverse('course:evaluation_index'),
      'link_text': "Pending Evaluations",
      'new_count': pending_evaluations.count()
    })
  return out
