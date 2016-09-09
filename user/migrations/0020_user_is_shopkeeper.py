# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_auto_20160908_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_shopkeeper',
            field=models.BooleanField(default=False, help_text=b'Shopkeepers can mark receipts as received.'),
        ),
    ]
