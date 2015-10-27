# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0017_auto_20151027_1127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enrollment',
            name='old_completed',
        ),
    ]
