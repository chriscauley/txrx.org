# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('redtape', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signature',
            name='date_typed',
            field=models.CharField(max_length=64, verbose_name=b'Type Todays Date'),
        ),
        migrations.AlterField(
            model_name='signature',
            name='name_typed',
            field=models.CharField(max_length=128, verbose_name=b'Type Your Name'),
        ),
    ]
