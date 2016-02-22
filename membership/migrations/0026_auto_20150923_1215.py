# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0025_auto_20150921_2301'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Membership',
            new_name='Level',
        ),
    ]
