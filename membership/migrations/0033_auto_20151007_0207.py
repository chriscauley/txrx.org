# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0032_remove_usermembership_orientation_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flag',
            name='reason',
            field=models.CharField(max_length=32, choices=[(b'recurring_payment_skipped', b'PayPal Skipped'), (b'recurring_payment_failed', b'PayPal Failed Recurring'), (b'recurring_payment_suspended', b'PayPal Suspended'), (b'recurring_payment_suspended_due_', b'PayPal End of Subscription'), (b'subscr_failed', b'PayPal Failed Subscription'), (b'subscr_eot', b'PayPal End of Term'), (b'manually_flagged', b'Manually Flagged')]),
        ),
    ]
