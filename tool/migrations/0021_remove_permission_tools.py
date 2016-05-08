# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0020_auto_20160502_2102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permission',
            name='tools',
        ),
    ]
