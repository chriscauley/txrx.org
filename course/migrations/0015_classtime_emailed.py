# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0014_session_notified'),
    ]

    operations = [
        migrations.AddField(
            model_name='classtime',
            name='emailed',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
