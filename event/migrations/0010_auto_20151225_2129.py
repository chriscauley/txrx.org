# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0009_event_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='url',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='eventoccurrence',
            name='url_override',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]
