# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20151004_0103'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_toolmaster',
            field=models.BooleanField(default=False, help_text=b'Toolmasters can give any user access to any Tool Criteria.'),
        ),
    ]
