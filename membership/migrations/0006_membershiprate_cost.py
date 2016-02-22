# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0005_auto_20150720_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='membershiprate',
            name='cost',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
