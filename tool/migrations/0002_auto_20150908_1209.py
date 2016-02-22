# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tool',
            name='materials',
            field=models.ManyToManyField(to='thing.Material', blank=True),
        ),
    ]
