# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-04-16 17:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thing', '0003_auto_20170409_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thing',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
