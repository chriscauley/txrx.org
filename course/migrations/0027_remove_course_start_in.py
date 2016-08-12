# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0026_auto_20160812_1444'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='start_in',
        ),
    ]
