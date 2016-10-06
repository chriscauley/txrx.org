# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0002_auto_20160927_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='has_checkoutitems',
            field=models.BooleanField(default=False),
        ),
    ]
