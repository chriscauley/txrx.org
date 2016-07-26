# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0042_auto_20160723_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='subscription',
            field=models.ForeignKey(blank=True, to='membership.Subscription', null=True),
        ),
        migrations.AlterField(
            model_name='container',
            name='kind',
            field=models.CharField(default=b'bay', max_length=64, choices=[(b'bay', b'Bay'), (b'drawer', b'Drawer')]),
        ),
        migrations.AlterField(
            model_name='container',
            name='status',
            field=models.CharField(default=b'used', max_length=16, choices=[(b'open', b'Open'), (b'used', b'Used'), (b'maintenance', b'Maintenance')]),
        ),
    ]
