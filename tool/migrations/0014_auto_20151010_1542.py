# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0013_auto_20151010_1436'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='criterion',
            options={'ordering': ('name',)},
        ),
    ]
