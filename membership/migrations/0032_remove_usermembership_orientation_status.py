# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0031_remove_usermembership_level'),
        ('user', '0006_auto_20151004_0103')
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermembership',
            name='orientation_status',
        ),
    ]
