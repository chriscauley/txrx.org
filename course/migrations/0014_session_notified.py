# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0013_auto_20151017_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='notified',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
