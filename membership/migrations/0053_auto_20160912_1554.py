# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0052_auto_20160912_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='level',
            name='holiday_access',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterUniqueTogether(
            name='leveldoorgroupschedule',
            unique_together=set([('level', 'doorgroup')]),
        ),
    ]
