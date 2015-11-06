# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0006_event_rsvp_cutoff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='repeat',
            field=models.CharField(blank=True, max_length=32, null=True, help_text=b'If your changing this, you will need to manually delete all future incorrect events.Repeating events are auto-generated every night.', choices=[(b'', b'No Repeat'), (b'weekly', b'Weekly'), (b'biweekly', b'Bi Weekly'), (b'triweekly', b'Tri Weekly'), (b'month-dow', b'Monthly (Nth weekday of every month)'), (b'month-number', b'Monthly (by day number)')]),
        ),
    ]
