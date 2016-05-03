# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def move_permissions(apps,schema_editor):
    for permission in apps.get_model('tool','permission').objects.all():
        for tool in permission.tools.all():
            tool.permission = permission
            tool.save()

class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0019_auto_20160502_2101'),
    ]

    operations = [
        migrations.RunPython(move_permissions)
    ]
