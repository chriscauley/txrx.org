# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_sessionproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sessionproduct',
            name='product_ptr',
        ),
        migrations.RemoveField(
            model_name='sessionproduct',
            name='session',
        ),
        migrations.DeleteModel(
            name='SessionProduct',
        ),
    ]
