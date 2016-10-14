# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_is_volunteer'),
        ('rfid', '0002_auto_20161014_1441'), #rfids are moved between apps here
    ]

    operations = [
        migrations.RemoveField(
            model_name='rfid',
            name='user',
        ),
        migrations.DeleteModel(
            name='RFID',
        ),
    ]
