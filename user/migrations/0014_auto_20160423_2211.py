# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_auto_20160423_1850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='rfid',
        ),
        migrations.AlterField(
            model_name='rfidcard',
            name='number',
            field=models.CharField(unique=True, max_length=16),
        ),
    ]
