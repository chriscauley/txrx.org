# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0033_auto_20151007_0207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flag',
            name='reason',
            field=models.CharField(max_length=64, choices=[(b'recurring_payment_skipped', b'PayPal Skipped'), (b'recurring_payment_failed', b'PayPal Failed Recurring'), (b'recurring_payment_suspended', b'PayPal Suspended'), (b'recurring_payment_suspended_due_to_max_failed_payment', b'PayPal End of Subscription'), (b'subscr_failed', b'PayPal Failed Subscription'), (b'subscr_eot', b'PayPal End of Term'), (b'manually_flagged', b'Manually Flagged')]),
        ),
    ]
