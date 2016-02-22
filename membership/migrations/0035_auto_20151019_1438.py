# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0034_auto_20151015_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flag',
            name='reason',
            field=models.CharField(max_length=64, choices=[(b'recurring_payment_skipped', b'PayPal Skipped'), (b'recurring_payment_failed', b'PayPal Failed Recurring'), (b'recurring_payment_suspended', b'PayPal Suspended'), (b'recurring_payment_suspended_due_to_max_failed_payment', b'PayPal End of Subscription'), (b'subscr_failed', b'PayPal Failed Subscription'), (b'subscr_eot', b'PayPal End of Term'), (b'manually_flagged', b'Manually Flagged'), (b'safety', b'Expiring Safety Criterion')]),
        ),
        migrations.AlterField(
            model_name='flag',
            name='status',
            field=models.CharField(default=b'new', max_length=32, choices=[(b'new', b'New'), (b'first_warning', b'Warned Once'), (b'second_warning', b'Warned Twice'), (b'final_warning', b'Canceled (Automatically)'), (b'canceled', b'Canceled (Manually)'), (b'resolved', b'Resolved'), (b'paid', b'Paid'), (b'safety_new', b'New'), (b'safety_emailed', b'Emailed'), (b'safety_expired', b'Expired (criterion revoked)'), (b'safety_completed', b'Completed (course taken)')]),
        ),
    ]
