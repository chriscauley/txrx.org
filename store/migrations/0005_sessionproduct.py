# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_enrollment_transaction_ids'),
        ('shop', '__first__'),
        ('store', '0004_auto_20150627_1330'),
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
