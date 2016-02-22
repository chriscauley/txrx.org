# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('redtape', '0002_auto_20151020_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='login_required',
            field=models.BooleanField(default=False, help_text=b'If checked, user must log into site before viewing/signing document'),
        ),
        migrations.AddField(
            model_name='signature',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
