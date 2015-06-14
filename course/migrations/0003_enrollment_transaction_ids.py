# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20150614_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='transaction_ids',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
