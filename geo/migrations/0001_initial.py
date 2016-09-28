# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import localflavor.us.models
import geo.widgets


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latlon', geo.widgets.LocationField(max_length=500, null=True, blank=True)),
                ('name', models.CharField(max_length=128)),
                ('state', localflavor.us.models.USStateField()),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Cities',
            },
        ),
        migrations.CreateModel(
            name='DXFEntity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('points', models.TextField()),
                ('dxftype', models.CharField(max_length=16)),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latlon', geo.widgets.LocationField(max_length=500, null=True, blank=True)),
                ('name', models.CharField(max_length=128, null=True, blank=True)),
                ('short_name', models.CharField(help_text=b'Optional. Alternative name for the calendar.', max_length=64, null=True, blank=True)),
                ('address', models.CharField(max_length=64, null=True, blank=True)),
                ('address2', models.CharField(max_length=64, null=True, blank=True)),
                ('zip_code', models.IntegerField(default=77007)),
                ('dxf', models.FileField(null=True, upload_to=b'floorplans', blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, null=True, blank=True)),
                ('short_name', models.CharField(help_text=b'Optional. Alternative name for the calendar.', max_length=64, null=True, blank=True)),
                ('in_calendar', models.BooleanField(default=True, verbose_name=b'can be scheduled for events')),
                ('map_key', models.CharField(max_length=1, null=True, blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='RoomGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=16)),
                ('color', models.CharField(max_length=32)),
            ],
        ),
    ]
