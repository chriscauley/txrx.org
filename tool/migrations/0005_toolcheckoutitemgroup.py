# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0004_auto_20161006_1138'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToolCheckoutItemGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('checkoutitems', models.ManyToManyField(to='tool.CheckoutItem')),
                ('tools', models.ManyToManyField(to='tool.Tool')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
