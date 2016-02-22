# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('redtape', '0003_auto_20151026_2326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signature',
            name='date',
        ),
        migrations.AddField(
            model_name='signature',
            name='completed',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='signature',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
