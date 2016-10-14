# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_coursecheckout'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursecheckout',
            name='categories',
            field=models.ManyToManyField(to='store.Category'),
        ),
    ]
