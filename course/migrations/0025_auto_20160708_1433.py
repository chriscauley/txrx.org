# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0024_auto_20160511_0054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseroomtime',
            name='hours_at',
            field=models.FloatField(default=0, help_text=b'Number of hours at location. 0 = Until class ends.'),
        ),
    ]
