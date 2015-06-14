# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import media.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('media', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(default=datetime.date.today)),
                ('end_date', models.DateField(blank=True)),
                ('name', models.CharField(max_length=64)),
                ('header', models.CharField(default=b'Featured Event', max_length=32)),
                ('active', models.BooleanField(default=True)),
                ('src', models.ImageField(upload_to=b'banners')),
                ('url', models.CharField(max_length=200)),
                ('weight', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, blank=True)),
                ('content', models.TextField(blank=True)),
                ('short_content', models.TextField(null=True, blank=True)),
                ('slug', models.SlugField(max_length=75)),
                ('status', models.CharField(default=0, max_length=30, choices=[(b'draft', b'Draft'), (b'published', b'Published')])),
                ('publish_dt', models.DateTimeField(null=True, verbose_name=b'Publish On')),
                ('create_dt', models.DateTimeField(auto_now_add=True)),
                ('update_dt', models.DateTimeField(auto_now=True)),
                ('featured', models.BooleanField(default=False, help_text=b"Featured blogs must have a photo or they won't appear at all.")),
                ('photo', models.ForeignKey(blank=True, to='media.Photo', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-featured', '-publish_dt'),
            },
            bases=(media.models.PhotosMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PressItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=64)),
                ('url', models.URLField(max_length=256)),
                ('publish_dt', models.DateField(verbose_name=b'Date')),
            ],
            options={
                'ordering': ('-publish_dt',),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='post',
            unique_together=set([('slug', 'user')]),
        ),
    ]
