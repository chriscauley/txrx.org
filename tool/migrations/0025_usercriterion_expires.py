# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0024_auto_20160621_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercriterion',
            name='expires',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
