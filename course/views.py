from django.template.response import TemplateResponse
from course.models import Course, Section, Term, Subject
from membership.models import Profile

filters = {
  "term": lambda: {
    "model": Term,
    "options": Term.objects.all(),
    "name": "Term",
    "slug": "term"
    },
  "subject": lambda: {
    "model": Subject,
    "options": Subject.objects.all(),
    "name": "Subject",
    "slug": "subject"
    }
  }

def index(request):
  term = Term.objects.all()[0]
  sections = Section.objects.filter(term=term)
  values = {
    'sections': sections,
    'filters': [filters['term'],filters['subject']]
    }
  return TemplateResponse(request,"course/classes.html",values)

def instructors(request,username=None):
  instructors = Profile.objects.list_instructors()
  values = {'instructors':instructors}
  return TemplateResponse(request,"instructors.html",values)
