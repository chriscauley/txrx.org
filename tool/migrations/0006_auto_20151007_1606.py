# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0012_auto_20151007_1606'),
        ('tool', '0005_auto_20151007_0207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='criterion',
            name='permission',
        ),
        migrations.AddField(
            model_name='criterion',
            name='courses',
            field=models.ManyToManyField(to='course.Course'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='criteria',
            field=models.ManyToManyField(help_text=b'All these criteria grants access to these tools.', related_name='+', to='tool.Criterion', blank=True),
        ),
    ]
