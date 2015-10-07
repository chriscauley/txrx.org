# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0011_auto_20151007_0207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursecriterion',
            name='course',
        ),
        migrations.RemoveField(
            model_name='coursecriterion',
            name='criterion',
        ),
        migrations.RemoveField(
            model_name='coursepermission',
            name='course',
        ),
        migrations.RemoveField(
            model_name='coursepermission',
            name='permission',
        ),
        migrations.DeleteModel(
            name='CourseCriterion',
        ),
        migrations.DeleteModel(
            name='CoursePermission',
        ),
    ]
