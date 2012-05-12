from django.template.response import TemplateResponse
from chores.models import Occurrence
import datetime

def home(request):
  now = datetime.datetime.now()
  occurrences = Occurrence.objects.filter(datetime__gte=now)
  values = {
    'complete_tasks': occurrences.filter(complete=True),
    'incomplete_tasks': occurrences.filter(complete=False),
    }
  return TemplateResponse(request,"home.html",values)
