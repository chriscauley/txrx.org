# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0009_auto_20151008_2124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permission',
            name='safety',
        ),
    ]
