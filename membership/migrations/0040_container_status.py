# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0039_remove_usermembership_paypal_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='status',
            field=models.CharField(default=b'open', max_length=16, choices=[(b'open', b'Open'), (b'used', b'Used'), (b'maintenance', b'Maintenance')]),
        ),
    ]
