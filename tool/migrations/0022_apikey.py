# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tool.models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0021_remove_permission_tools'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(default=tool.models.new_key, max_length=30)),
            ],
        ),
    ]
