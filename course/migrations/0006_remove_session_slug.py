# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_auto_20150908_1209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='slug',
        ),
    ]
