# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tool', '0010_remove_permission_safety'),
    ]

    operations = [
        migrations.AddField(
            model_name='criterion',
            name='supervisors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
