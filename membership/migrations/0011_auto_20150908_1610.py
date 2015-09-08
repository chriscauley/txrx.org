# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0010_auto_20150908_1505'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MembershipGroup',
            new_name='Group',
        ),
        migrations.RenameField(
            model_name='membership',
            old_name='membershipgroup',
            new_name='group',
        ),
    ]
