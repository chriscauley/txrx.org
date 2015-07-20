# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0003_membershipproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membershipproduct',
            name='cost',
        ),
        migrations.RemoveField(
            model_name='membershiprate',
            name='cost',
        ),
        migrations.AlterField(
            model_name='membershiprate',
            name='months',
            field=models.IntegerField(default=1, choices=[(1, b'Monthly'), (12, b'Yearly')]),
            preserve_default=True,
        ),
    ]
