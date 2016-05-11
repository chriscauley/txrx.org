# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0023_auto_20160511_0015'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courseroomtime',
            options={'ordering': ('day', 'order')},
        ),
        migrations.RemoveField(
            model_name='courseroomtime',
            name='time',
        ),
        migrations.AddField(
            model_name='courseroomtime',
            name='hours_at',
            field=models.FloatField(default=0.5, help_text=b'Number of hours at location.'),
        ),
        migrations.AddField(
            model_name='courseroomtime',
            name='order',
            field=models.IntegerField(default=999),
        ),
    ]
