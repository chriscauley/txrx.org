# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0018_criterion_documents'),
    ]

    operations = [
        migrations.AddField(
            model_name='tool',
            name='permission',
            field=models.ForeignKey(blank=True, to='tool.Permission', null=True),
        ),
        migrations.AlterField(
            model_name='permission',
            name='tools',
            field=models.ManyToManyField(related_name='+', to='tool.Tool', blank=True),
        ),
    ]
