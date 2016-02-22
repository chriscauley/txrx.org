# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0011_auto_20150908_1610'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scheduledpayment',
            name='subscription',
        ),
        migrations.AddField(
            model_name='subscription',
            name='paid_until',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.DeleteModel(
            name='ScheduledPayment',
        ),
    ]
