# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redtape', '0013_auto_20160822_2141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signature',
            name='signature',
        ),
    ]
