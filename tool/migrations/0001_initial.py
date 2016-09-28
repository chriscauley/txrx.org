# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import colorful.fields
import tool.models
import store.models
import wmd.models
import media.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(default=tool.models.new_key, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Criterion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='DoorGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('description', models.TextField(help_text=b'List all the doors this can open.')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('color', colorful.fields.RGBColorField()),
                ('column', models.IntegerField(choices=[(0, b'left'), (1, b'right')])),
                ('row', models.IntegerField()),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, blank=True)),
                ('date', models.DateField()),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=99999)),
                ('name', models.CharField(max_length=128)),
                ('description', wmd.models.MarkDownField(null=True, blank=True)),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(media.models.PhotosMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('abbreviation', models.CharField(help_text=b'For badge.', max_length=16)),
                ('order', models.IntegerField(default=999)),
            ],
            options={
                'ordering': ('group', 'order'),
            },
        ),
        migrations.CreateModel(
            name='PermissionSchedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
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
                ('start', models.CharField(default=b'1000', max_length=4)),
                ('end', models.CharField(default=b'2200', max_length=4)),
            ],
            options={
                'ordering': ('dow',),
            },
        ),
        migrations.CreateModel(
            name='TaggedTool',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.IntegerField()),
                ('order', models.IntegerField(default=9999)),
            ],
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=99999)),
                ('name', models.CharField(max_length=128)),
                ('make', models.CharField(max_length=64, null=True, blank=True)),
                ('model', models.CharField(max_length=32, null=True, blank=True)),
                ('description', wmd.models.MarkDownField(null=True, blank=True)),
                ('est_price', models.FloatField(null=True, blank=True)),
                ('functional', models.BooleanField(default=True)),
                ('repair_date', models.DateField(null=True, blank=True)),
            ],
            options={
                'ordering': ('lab', 'order'),
            },
            bases=(store.models.ConsumablesMixin, media.models.PhotosMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ToolLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=99999)),
                ('title', models.CharField(max_length=64)),
                ('url', models.URLField()),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='UserCriterion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('expires', models.DateTimeField(null=True, blank=True)),
                ('object_id', models.IntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('criterion', models.ForeignKey(to='tool.Criterion')),
            ],
        ),
    ]
