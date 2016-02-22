# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0010_remove_session_time_string'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecriterion',
            name='course',
            field=models.ForeignKey(help_text=b'Completing this course (or any other in this list) meets this criterion', to='course.Course'),
        ),
        migrations.AlterField(
            model_name='coursepermission',
            name='course',
            field=models.ForeignKey(help_text=b'Completing this course (and all associated criteria) grants this permission.', to='course.Course'),
        ),
    ]
