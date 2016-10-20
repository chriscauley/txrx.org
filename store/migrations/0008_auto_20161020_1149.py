# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20161020_1140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='consumable',
            name='_categories',
        ),
        migrations.RemoveField(
            model_name='coursecheckout',
            name='_categories',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
