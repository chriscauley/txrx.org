# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0012_auto_20151007_1606'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursecompletion',
            name='course',
        ),
        migrations.RemoveField(
            model_name='coursecompletion',
            name='user',
        ),
        migrations.DeleteModel(
            name='CourseCompletion',
        ),
    ]
