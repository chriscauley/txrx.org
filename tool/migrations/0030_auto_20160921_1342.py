# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wmd.models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0029_holiday'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='doorgroup',
            options={'ordering': ('id',)},
        ),
        migrations.AlterField(
            model_name='lab',
            name='description',
            field=wmd.models.MarkDownField(null=True, blank=True),
        ),
    ]
