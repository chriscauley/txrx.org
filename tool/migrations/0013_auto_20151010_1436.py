# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0012_remove_criterion_supervisors'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='permission',
            options={'ordering': ('room', 'order')},
        ),
        migrations.AddField(
            model_name='permission',
            name='abbreviation',
            field=models.CharField(default='arst', help_text=b'For badge.', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='permission',
            name='order',
            field=models.IntegerField(default=999),
        ),
    ]
