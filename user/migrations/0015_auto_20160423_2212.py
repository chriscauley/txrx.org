# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_auto_20160423_2211'),
    ]

    operations = [
        migrations.RenameModel(
            "RFIDCard","RFID"
        ),
    ]
