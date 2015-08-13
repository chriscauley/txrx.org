# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0009_auto_20150812_1756'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='membershipchange',
            options={'ordering': ('datetime',)},
        ),
        migrations.AddField(
            model_name='membershipchange',
            name='date_override',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membershipchange',
            name='payment_method',
            field=models.CharField(default=b'admin', max_length=16, choices=[(b'paypal', b'PayPalIPN'), (b'admin', b'Admin (manual)')]),
            preserve_default=True,
        ),
    ]
