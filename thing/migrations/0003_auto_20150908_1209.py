# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thing', '0002_auto_20150614_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thing',
            name='materials',
            field=models.ManyToManyField(to='thing.Material', blank=True),
        ),
    ]
