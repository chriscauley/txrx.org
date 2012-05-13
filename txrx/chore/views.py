from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from chore.models import Occurrence
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages

from .models import Task
import datetime

def index(request):
  now = datetime.datetime.now()
  occurrences = Occurrence.objects.filter(datetime__gte=now)
  values = {
    'complete_tasks': occurrences.filter(complete=True),
    'incomplete_tasks': occurrences.filter(complete=False),
    }
  return TemplateResponse(request,"chore/index.html",values)

@user_passes_test(lambda u: u.is_superuser)
def update_occurrences(request,_id):
  task = Task.objects.get(id=_id)
  task.update_occurrences()
  messages.success(request,"Occurences for this task have been updated.")
  return HttpResponseRedirect("/admin/chore/task/%s/"%_id)

@login_required
def assign(request,_id=None):
  pass

@login_required
def complete(request,_id=None):
  pass
