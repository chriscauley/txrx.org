# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0004_auto_20151004_1324'),
        ('course', '0007_coursepermission'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCriterion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course', models.ForeignKey(to='course.Course')),
                ('criterion', models.ForeignKey(to='tool.Criterion')),
            ],
        ),
    ]
