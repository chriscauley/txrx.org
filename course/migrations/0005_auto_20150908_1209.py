# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_sessionproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='enrollment',
            field=models.OneToOneField(to='course.Enrollment'),
        ),
    ]
