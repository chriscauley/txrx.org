# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0046_auto_20160726_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='status',
            field=models.CharField(default=b'used', max_length=16, choices=[(b'open', b'Open'), (b'used', b'Used'), (b'email', b'Needs Email'), (b'emailed', b'Emailed'), (b'maintenance', b'Maintenance')]),
        ),
        migrations.AlterField(
            model_name='container',
            name='subscription',
            field=models.OneToOneField(null=True, blank=True, to='membership.Subscription'),
        ),
    ]
