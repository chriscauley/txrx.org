# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0008_auto_20151007_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='criteria',
            field=models.ManyToManyField(help_text=b'Requires all these criteria to access these tools.', to='tool.Criterion', blank=True),
        ),
    ]
