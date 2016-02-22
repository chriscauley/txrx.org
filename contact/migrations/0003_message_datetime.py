# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_auto_20150908_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 5, 15, 35, 20, 264856), auto_now_add=True),
            preserve_default=False,
        ),
    ]
