# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0004_auto_20151004_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='criterion',
            name='permission',
            field=models.ForeignKey(blank=True, to='tool.Permission', help_text=b'Possessing this permission meets this criterion', null=True),
        ),
        migrations.AlterField(
            model_name='permission',
            name='criteria',
            field=models.ManyToManyField(help_text=b'All these criteria (and a course) grants access to these tools.', related_name='+', to='tool.Criterion', blank=True),
        ),
        migrations.AlterField(
            model_name='permission',
            name='tools',
            field=models.ManyToManyField(to='tool.Tool', blank=True),
        ),
    ]
