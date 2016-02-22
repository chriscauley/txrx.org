# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '__first__'),
        ('membership', '0002_auto_20150614_1510'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipProduct',
            fields=[
                ('product_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='shop.Product')),
                ('cost', models.IntegerField()),
                ('description', models.CharField(max_length=128)),
                ('order', models.IntegerField(default=0)),
                ('membership', models.ForeignKey(to='membership.Membership')),
            ],
            options={
                'ordering': ('order',),
            },
            bases=('shop.product',),
        ),
    ]
