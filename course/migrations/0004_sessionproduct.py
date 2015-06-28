# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '__first__'),
        ('course', '0003_enrollment_transaction_ids'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionProduct',
            fields=[
                ('product_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='shop.Product')),
                ('session', models.OneToOneField(to='course.Session')),
            ],
            options={
                'ordering': ('pk',),
            },
            bases=('shop.product',),
        ),
    ]
