# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0016_auto_20150917_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='userflag',
            name='emailed',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
