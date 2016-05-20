# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0038_level_permission_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermembership',
            name='paypal_email',
        ),
    ]
