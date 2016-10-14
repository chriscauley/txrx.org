# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rfid', '0002_auto_20161014_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rfid',
            name='added',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
