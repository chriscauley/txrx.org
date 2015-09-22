# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0024_auto_20150920_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='payment_method',
            field=models.CharField(default=b'cash', max_length=16, choices=[(b'paypal', b'PayPalIPN'), (b'cash', b'Cash/Check'), (b'adjustment', b'Adjustment (gift from lab)'), (b'refund', b'Refund'), (b'legacy', b'Legacy (PayPal)')]),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='product',
            field=models.ForeignKey(default=1, to='membership.Product'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='subscr_id',
            field=models.CharField(help_text=b'Only used with PayPal subscriptions. Do not touch.', max_length=20, null=True, blank=True),
        ),
    ]
