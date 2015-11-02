# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_event_max_rsvp'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='rsvp_cutoff',
            field=models.FloatField(default=0, help_text=b'Number of days before event when RSVP is cut off (eg 0.5 means "You must rsvp 12 hours before this event")'),
        ),
    ]
