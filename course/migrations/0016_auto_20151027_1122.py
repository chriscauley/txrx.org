# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

class Migration(migrations.Migration):

    dependencies = [
        ('course', '0015_classtime_emailed'),
    ]
    operations = [
        migrations.RenameField(
            model_name='enrollment',
            old_name='completed',
            new_name='old_completed',
        ),
        migrations.AddField(
            model_name='enrollment',
            name='completed',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
