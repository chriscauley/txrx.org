# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0029_auto_20150930_1732'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermembership',
            name='end',
        ),
        migrations.RemoveField(
            model_name='usermembership',
            name='rfid',
        ),
        migrations.RemoveField(
            model_name='usermembership',
            name='start',
        ),
    ]
