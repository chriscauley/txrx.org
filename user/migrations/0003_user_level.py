# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0030_auto_20151003_2114'),
        ('user', '0002_auto_20150908_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='level',
            field=models.ForeignKey(default=1, to='membership.Level'),
        ),
    ]
