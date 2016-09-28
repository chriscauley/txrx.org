# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import wmd.models
import media.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'ordering': ('-datetime',),
            },
        ),
        migrations.CreateModel(
            name='CheckInPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'ordering': ('room__name',),
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, null=True, blank=True)),
                ('url', models.CharField(max_length=256, null=True, blank=True)),
                ('short_name', models.CharField(help_text=b'Optional. Alternative name for the calendar.', max_length=64, null=True, blank=True)),
                ('description', wmd.models.MarkDownField(null=True, blank=True)),
                ('repeat', models.CharField(blank=True, max_length=32, null=True, help_text=b'If your changing this, you will need to manually delete all future incorrect events.Repeating events are auto-generated every night.', choices=[(b'', b'No Repeat'), (b'weekly', b'Weekly'), (b'biweekly', b'Bi Weekly'), (b'triweekly', b'Tri Weekly'), (b'month-dow', b'Monthly (Nth weekday of every month)'), (b'month-number', b'Monthly (by day number)')])),
                ('no_conflict', models.BooleanField(default=False, help_text=b'If true, this class will not raise conflict warnings for events in the same room.')),
                ('hidden', models.BooleanField(default=False)),
                ('allow_rsvp', models.BooleanField(default=True)),
                ('rsvp_cutoff', models.FloatField(default=0, help_text=b'Number of days before event when RSVP is cut off (eg 0.5 means "You must rsvp 12 hours before this event")')),
                ('max_rsvp', models.IntegerField(default=128)),
                ('icon', models.CharField(max_length=16, choices=[(b'public', b'Open to the public'), (b'private', b'Private - Invitation only'), (b'rsvp', b'RSVP Required')])),
            ],
            bases=(media.models.PhotosMixin, models.Model),
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
                ('url_override', models.CharField(max_length=256, null=True, blank=True)),
            ],
            options={
                'ordering': ('start',),
            },
            bases=(media.models.PhotosMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RSVP',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.IntegerField()),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('emailed', models.DateTimeField(null=True, blank=True)),
                ('quantity', models.IntegerField(default=0)),
                ('completed', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
