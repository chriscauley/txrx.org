from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Task
from django.contrib import messages

@user_passes_test(lambda u: u.is_superuser)
def update_occurrences(request,_id):
  task = Task.objects.get(id=_id)
  task.update_occurrences()
  messages.success(request,"Occurences for this task have been updated.")
  return HttpResponseRedirect("/admin/chores/task/%s/"%_id)

@login_required
def assign(request,_id=None):
  pass

@login_required
def complete(request,_id=None):
  pass
