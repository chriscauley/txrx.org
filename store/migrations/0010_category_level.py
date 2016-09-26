# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_taggedconsumable'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='level',
            field=models.IntegerField(default=0),
        ),
    ]
