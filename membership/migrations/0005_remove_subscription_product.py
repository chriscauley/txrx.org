# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0004_auto_20161021_1111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='product',
        ),
    ]
