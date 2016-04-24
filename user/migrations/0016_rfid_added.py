# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_auto_20160423_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='rfid',
            name='added',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 23, 22, 18, 42, 376943), auto_now_add=True),
            preserve_default=False,
        ),
    ]
