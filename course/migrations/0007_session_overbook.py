# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_courseenrollment_failed'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='overbook',
            field=models.IntegerField(default=0, help_text=b'This session will not appear as overbooked if it is less than X seats overbooked.'),
        ),
    ]
