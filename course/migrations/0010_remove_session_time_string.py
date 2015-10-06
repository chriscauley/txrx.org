# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0009_auto_20151004_1332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='time_string',
        ),
    ]
