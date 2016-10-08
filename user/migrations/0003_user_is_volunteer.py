# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_volunteer',
            field=models.BooleanField(default=False, help_text=b'Only used for filtering, currently'),
        ),
    ]
