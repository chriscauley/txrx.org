# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0027_doorgroup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scheduleday',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='scheduleday',
            name='start_time',
        ),
        migrations.AddField(
            model_name='scheduleday',
            name='end',
            field=models.CharField(default=b'2200', max_length=4),
        ),
        migrations.AddField(
            model_name='scheduleday',
            name='start',
            field=models.CharField(default=b'1000', max_length=4),
        ),
    ]
