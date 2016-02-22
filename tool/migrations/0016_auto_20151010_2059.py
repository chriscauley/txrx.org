# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import colorful.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0015_auto_20151010_2015'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ('name',)},
        ),
        migrations.AlterField(
            model_name='group',
            name='color',
            field=colorful.fields.RGBColorField(),
        ),
    ]
