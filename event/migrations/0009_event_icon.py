# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0008_auto_20151206_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='icon',
            field=models.CharField(default='public', max_length=16, choices=[(b'public', b'Open to the public'), (b'private', b'Private - Invitation only'), (b'rsvp', b'RSVP Required')]),
            preserve_default=False,
        ),
    ]
