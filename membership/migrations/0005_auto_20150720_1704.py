# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0004_auto_20150720_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membershipproduct',
            name='description',
        ),
        migrations.AddField(
            model_name='membershipproduct',
            name='months',
            field=models.IntegerField(default=1, choices=[(1, b'Monthly'), (12, b'Yearly')]),
            preserve_default=True,
        ),
    ]
