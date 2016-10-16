# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_courseenrollment'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseenrollment',
            name='failed',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
