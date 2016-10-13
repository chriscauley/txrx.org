# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import datetime

def mark_instructor_completed(apps, schema_editor):
  for session in apps.get_model('course','session').objects.all():
    past = datetime.datetime.now() > session.last_date
    if not past or session.instructor_completed:
      continue
    enrollments = session.enrollment_set.all().count()
    completed = session.enrollment_set.filter(completed__isnull=False).count()
    if not completed:
      continue
    if enrollments == completed:
      session.instructor_completed = datetime.date.today(); session.save()
      continue
    if enrollments < completed * 2:
      session.instructor_completed = datetime.date.today(); session.save()
      continue
    if session.course.id == settings.SAFETY_ID:
      session.instructor_completed = datetime.date.today(); session.save()
      continue
    if completed > 4:
      session.instructor_completed = datetime.date.today(); session.save()
      continue

class Migration(migrations.Migration):
  dependencies = [
    ('course', '0003_session_instructor_completed'),
  ]
  operations = [
    migrations.RunPython(mark_instructor_completed,lambda *args: None)
  ]
