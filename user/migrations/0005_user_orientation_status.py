# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20151004_0039'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='orientation_status',
            field=models.CharField(default=b'new', max_length=32, choices=[(b'new', b'New'), (b'emailed', b'Emailed'), (b'scheduled', b'scheduled'), (b'oriented', b'Oriented')]),
        ),
    ]
