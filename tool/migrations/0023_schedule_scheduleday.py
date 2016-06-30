# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0022_apikey'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleDay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dow', models.IntegerField(choices=[(0, b'Su'), (1, b'Mo'), (2, b'Tu'), (3, b'We'), (4, b'Th'), (5, b'Fr'), (6, b'Sa')])),
                ('start_time', models.TimeField(default=b'10:00')),
                ('end_time', models.TimeField(default=b'22:00')),
                ('schedule', models.ForeignKey(to='tool.Schedule')),
            ],
        ),
    ]
