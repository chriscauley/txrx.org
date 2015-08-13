# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0010_auto_20150812_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='membershipchange',
            name='subscr_id',
            field=models.CharField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
    ]
