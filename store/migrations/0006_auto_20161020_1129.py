# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_coursecheckout_categories'),
    ]

    operations = [
        migrations.RenameField(
            model_name='consumable',
            old_name='categories',
            new_name='_categories',
        ),
        migrations.RenameField(
            model_name='coursecheckout',
            old_name='categories',
            new_name='_categories',
        ),
    ]
