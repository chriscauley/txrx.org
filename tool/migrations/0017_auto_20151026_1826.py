# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0016_auto_20151010_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='criterion',
            name='courses',
            field=models.ManyToManyField(to='course.Course', blank=True),
        ),
    ]
