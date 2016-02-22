from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from course.models import Course, Session
import json, datetime

def course_json(request,course_id):
  course = get_object_or_404(Course,id=course_id)
  return HttpResponse(json.dumps(course.as_json))

def past_sessions_json(request):
  course = get_object_or_404(Course,id=request.GET.get('id',None))
  return HttpResponse(json.dumps([s.as_json for s in course.archived_sessions]))

def get_needed_sessions():
  month_ago = datetime.date.today()-datetime.timedelta(20)
  return Session.objects.exclude(needed="").exclude(needed_completed__lte=month_ago)

@staff_member_required
def needed_json(request):
  if request.GET.get("complete"):
    Session.objects.filter(id=request.GET["complete"]).update(needed_completed=datetime.date.today())
  if request.GET.get("incomplete"):
    Session.objects.filter(id=request.GET["incomplete"]).update(needed_completed=None)
  sessions = get_needed_sessions()
  sessions_jsons = [{
    'course': unicode(s.course),
    'user': s.user.get_full_name(),
    'first_date': s.first_date.strftime("%m/%d/%Y"),
    'needed': s.needed,
    'needed_completed': s.needed_completed.strftime("%m/%d/%Y") if s.needed_completed else None,
    'id': s.id
  } for s in sessions]
  return HttpResponse(json.dumps(sessions_jsons))
