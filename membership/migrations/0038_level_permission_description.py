# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0037_auto_20151029_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='level',
            name='permission_description',
            field=models.TextField(default=b'', blank=True),
        ),
    ]
