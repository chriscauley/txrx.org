# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('follow', models.BooleanField(default=False, help_text=b'Searches for photos belonging to this when update_instagram is run')),
                ('approved', models.BooleanField(default=False, help_text=b'USE WITH CATUION!! Automatically mark all photos of this type as approved.')),
                ('name', models.CharField(max_length=128)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('iid', models.CharField(max_length=32)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstagramPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('thumbnail', models.ImageField(null=True, upload_to=b'uploads/instagram', blank=True)),
                ('low_resolution', models.ImageField(null=True, upload_to=b'uploads/instagram', blank=True)),
                ('standard_resolution', models.ImageField(null=True, upload_to=b'uploads/instagram', blank=True)),
                ('caption', models.CharField(max_length=255, null=True, blank=True)),
                ('created_time', models.IntegerField()),
                ('iid', models.CharField(max_length=32)),
                ('approved', models.BooleanField(default=False)),
                ('rejected', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-created_time',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstagramTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('follow', models.BooleanField(default=False, help_text=b'Searches for photos belonging to this when update_instagram is run')),
                ('approved', models.BooleanField(default=False, help_text=b'USE WITH CATUION!! Automatically mark all photos of this type as approved.')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstagramUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('follow', models.BooleanField(default=False, help_text=b'Searches for photos belonging to this when update_instagram is run')),
                ('approved', models.BooleanField(default=False, help_text=b'USE WITH CATUION!! Automatically mark all photos of this type as approved.')),
                ('iid', models.CharField(max_length=32)),
                ('username', models.CharField(max_length=128, null=True, blank=True)),
                ('profile_picture', models.ImageField(null=True, upload_to=b'uploads/instagram', blank=True)),
                ('full_name', models.CharField(max_length=128, null=True, blank=True)),
                ('bio', models.TextField(null=True, blank=True)),
                ('website', models.URLField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
