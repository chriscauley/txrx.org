# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0003_auto_20151003_2211'),
        ('course', '0006_remove_session_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoursePermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course', models.ForeignKey(to='course.Course')),
                ('permission', models.ForeignKey(to='tool.Permission')),
            ],
        ),
    ]
