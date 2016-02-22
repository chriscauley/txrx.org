# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

import datetime

def completed2datetime(apps,schema_editor):
    es = apps.get_model('course','enrollment').objects.filter(old_completed=True)
    es.update(completed=datetime.datetime.now())
        

class Migration(migrations.Migration):

    dependencies = [
        ('course', '0016_auto_20151027_1122'),
    ]

    operations = [
        migrations.RunPython(completed2datetime)
    ]
