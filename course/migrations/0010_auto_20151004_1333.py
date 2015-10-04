# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0009_auto_20151004_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='fee',
            field=models.IntegerField(default=0),
        ),
    ]
