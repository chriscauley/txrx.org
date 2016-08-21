# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0050_auto_20160819_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='drop.Product'),
        ),
    ]
