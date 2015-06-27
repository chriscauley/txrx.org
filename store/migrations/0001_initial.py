# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consumable',
            fields=[
                ('product_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='shop.Product')),
            ],
            options={
            },
            bases=('shop.product',),
        ),
    ]
