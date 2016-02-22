# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0027_auto_20150923_1225'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SubscriptionFlag',
            new_name='Flag',
        ),
    ]
