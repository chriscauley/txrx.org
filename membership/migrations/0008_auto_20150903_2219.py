# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0007_auto_20150903_1845'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscription',
            options={'ordering': ('created',)},
        ),
        migrations.RenameField(
            model_name='subscription',
            old_name='cancelled',
            new_name='canceled',
        ),
    ]
