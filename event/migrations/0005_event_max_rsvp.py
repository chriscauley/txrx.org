# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_event_allow_rsvp'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='max_rsvp',
            field=models.IntegerField(default=128),
        ),
    ]
