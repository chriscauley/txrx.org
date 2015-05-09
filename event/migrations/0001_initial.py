# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wmd.models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, null=True, blank=True)),
                ('short_name', models.CharField(help_text=b'Optional. Alternative name for the calendar.', max_length=64, null=True, blank=True)),
                ('description', wmd.models.MarkDownField(null=True, blank=True)),
                ('repeat', models.CharField(blank=True, max_length=32, null=True, help_text=b'If your changing this, you will need to manually delete all future incorrect events. Repeating events are auto-generated every night.', choices=[(b'', b'No Repeat'), (b'weekly', b'Weekly'), (b'biweekly', b'Bi Weekly'), (b'triweekly', b'Tri Weekly'), (b'month-dow', b'Monthly (Nth weekday of every month)'), (b'month-number', b'Monthly (by day number)')])),
                ('no_conflict', models.BooleanField(default=False, help_text=b'If true, this class will not raise conflict warnings for events in the same room.')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventOccurrence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField()),
                ('end_time', models.TimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('publish_dt', models.DateTimeField(default=datetime.datetime.now)),
                ('name_override', models.CharField(max_length=128, null=True, blank=True)),
                ('description_override', wmd.models.MarkDownField(null=True, blank=True)),
                ('event', models.ForeignKey(to='event.Event')),
            ],
            options={
                'ordering': ('start',),
            },
            bases=(models.Model,),
        ),
    ]
