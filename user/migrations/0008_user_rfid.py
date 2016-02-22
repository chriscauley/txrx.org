# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_user_is_toolmaster'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='rfid',
            field=models.CharField(max_length=16, null=True, blank=True),
        ),
    ]
