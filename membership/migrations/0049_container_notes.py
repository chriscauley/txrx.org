# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0048_auto_20160727_1246'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='notes',
            field=models.TextField(null=True, blank=True),
        ),
    ]
