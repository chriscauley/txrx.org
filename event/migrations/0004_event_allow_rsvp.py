# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_auto_20151023_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='allow_rsvp',
            field=models.BooleanField(default=True),
        ),
    ]
