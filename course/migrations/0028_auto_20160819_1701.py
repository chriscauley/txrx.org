# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20160819_1641'),
        ('course', '0027_remove_course_start_in'),
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
