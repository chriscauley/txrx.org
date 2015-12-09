from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from course.models import Course
import json

def course_json(request,course_id):
  course = get_object_or_404(Course,id=course_id)
  return HttpResponse(json.dumps(course.as_json))

def past_sessions_json(request):
  course = get_object_or_404(Course,id=request.GET.get('id',None))
  return HttpResponse(json.dumps([s.as_json for s in course.archived_sessions]))
