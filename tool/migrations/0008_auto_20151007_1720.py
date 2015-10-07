# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('tool', '0007_usercriterion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercriterion',
            name='source',
        ),
        migrations.AddField(
            model_name='usercriterion',
            name='content_type',
            field=models.ForeignKey(default=1, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usercriterion',
            name='object_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
