# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('thing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='thing',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='material',
            name='parent',
            field=models.ForeignKey(blank=True, to='thing.Material', null=True),
            preserve_default=True,
        ),
    ]
