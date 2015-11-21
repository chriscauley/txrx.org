from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from course.models import Course
import json

def course_json(request,course_id):
  course = get_object_or_404(Course,id=course_id)
  return HttpResponse(json.dumps(course.as_json))
