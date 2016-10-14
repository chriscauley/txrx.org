# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rfid', '0003_auto_20161014_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='rfidlog',
            name='data',
            field=models.TextField(default=b'{}'),
        ),
    ]
