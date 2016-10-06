# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0002_auto_20160927_2109'),
        ('tool', '0002_auto_20160927_2109'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckoutItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('room', models.ForeignKey(to='geo.Room')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
