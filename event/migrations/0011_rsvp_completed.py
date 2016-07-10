# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0010_auto_20151225_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='rsvp',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
