# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0020_auto_20160206_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='course',
            field=models.ForeignKey(default=1, to='course.Course'),
            preserve_default=False,
        ),
    ]
