# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumable',
            name='purchase_quantity',
            field=models.IntegerField(default=1, help_text=b'Amount purchased (by us when restocking) at a time. Used to make the refill process quick.'),
        ),
    ]
