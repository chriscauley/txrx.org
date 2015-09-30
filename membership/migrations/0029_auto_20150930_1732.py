# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0028_auto_20150924_1542'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscription',
            options={'ordering': ('-created',)},
        ),
        migrations.RemoveField(
            model_name='usermembership',
            name='waiver',
        ),
        migrations.AddField(
            model_name='usermembership',
            name='rfid',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='flag',
            name='status',
            field=models.CharField(default=b'new', max_length=32, choices=[(b'new', b'New'), (b'first_warning', b'Warned Once'), (b'second_warning', b'Warned Twice'), (b'final_warning', b'Canceled (Automatically)'), (b'canceled', b'Canceled (Manually)'), (b'resolved', b'Resolved'), (b'paid', b'Paid')]),
        ),
    ]
