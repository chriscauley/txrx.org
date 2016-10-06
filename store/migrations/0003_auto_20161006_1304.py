# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_toolconsumablegroup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taggedconsumable',
            name='consumable',
        ),
        migrations.RemoveField(
            model_name='taggedconsumable',
            name='content_type',
        ),
        migrations.DeleteModel(
            name='TaggedConsumable',
        ),
    ]
