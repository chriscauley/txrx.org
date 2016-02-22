# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0019_session_private'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='needed',
            field=models.TextField(default=b'', verbose_name=b'What is needed?', blank=True),
        ),
        migrations.AddField(
            model_name='session',
            name='needed_completed',
            field=models.DateField(null=True, blank=True),
        ),
    ]
