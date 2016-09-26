# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0028_auto_20160819_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='level',
            field=models.IntegerField(default=0),
        ),
    ]
