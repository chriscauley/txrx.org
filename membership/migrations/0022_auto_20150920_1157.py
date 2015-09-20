# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0021_auto_20150919_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermembership',
            name='orientation_status',
            field=models.CharField(default=b'new', max_length=32, choices=[(b'new', b'New'), (b'emailed', b'Emailed'), (b'scheduled', b'scheduled'), (b'oriented', b'Oriented')]),
        ),
    ]
