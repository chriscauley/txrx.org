# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0022_auto_20150920_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='transaction_id',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='subscriptionflag',
            name='reason',
            field=models.CharField(max_length=32, choices=[(b'recurring_payment_skipped', b'PayPal Skipped'), (b'recurring_payment_failed', b'PayPal Failed Recurring'), (b'recurring_payment_suspended', b'PayPal Suspended'), (b'subscr_failed', b'PayPal Failed Subscription'), (b'subscr_eot', b'PayPal End of Term'), (b'manually_flagged', b'Manually Flagged')]),
        ),
    ]
