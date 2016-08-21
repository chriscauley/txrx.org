# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20160708_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumable',
            name='product_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='drop.Product'),
        ),
    ]
