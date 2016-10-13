# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20160927_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='instructor_completed',
            field=models.DateField(null=True, blank=True),
        ),
    ]
