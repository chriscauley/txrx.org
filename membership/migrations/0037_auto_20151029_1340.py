# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0036_auto_20151021_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='level',
            name='cost_per_credit',
            field=models.DecimalField(default=0, max_digits=30, decimal_places=2),
        ),
        migrations.AddField(
            model_name='level',
            name='custom_training_cost',
            field=models.DecimalField(default=0, max_digits=30, decimal_places=2),
        ),
        migrations.AddField(
            model_name='level',
            name='custom_training_max',
            field=models.DecimalField(default=0, max_digits=30, decimal_places=2),
        ),
        migrations.AddField(
            model_name='level',
            name='machine_credits',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='level',
            name='simultaneous_users',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='months',
            field=models.IntegerField(default=1, choices=[(1, b'Monthly'), (3, b'Quarterly'), (6, b'Biannually'), (12, b'Yearly')]),
        ),
    ]
