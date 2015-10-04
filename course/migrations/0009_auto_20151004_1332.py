# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_coursecriterion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='fee',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
