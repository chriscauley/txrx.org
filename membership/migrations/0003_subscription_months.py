# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0002_auto_20160927_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='months',
            field=models.IntegerField(default=1, choices=[(1, b'Monthly'), (3, b'Quarterly'), (6, b'Biannually'), (12, b'Yearly')]),
        ),
    ]
