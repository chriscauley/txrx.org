# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redtape', '0016_auto_20160826_1630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentfield',
            name='slug',
        ),
        migrations.AddField(
            model_name='documentfield',
            name='name',
            field=models.CharField(help_text=b'For fields with the same label', max_length=64, null=True, blank=True),
        ),
    ]
