# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0021_auto_20160220_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='no_discount',
            field=models.BooleanField(default=False),
        ),
    ]
