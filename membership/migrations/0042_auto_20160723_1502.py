# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0041_auto_20160723_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
