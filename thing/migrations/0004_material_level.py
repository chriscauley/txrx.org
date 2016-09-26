# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thing', '0003_auto_20150908_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='level',
            field=models.IntegerField(default=0),
        ),
    ]
