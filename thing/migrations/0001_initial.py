# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wmd.models
import media.models
import tool.models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('order', models.FloatField(default=0)),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Thing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('description', wmd.models.MarkDownField(null=True, blank=True)),
                ('publish_dt', models.DateTimeField(auto_now_add=True)),
                ('featured', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=False)),
                ('parent_link', models.URLField(null=True, blank=True)),
                ('materials', models.ManyToManyField(to='thing.Material', null=True, blank=True)),
                ('parent', models.ForeignKey(blank=True, to='thing.Thing', null=True)),
                ('session', models.ForeignKey(blank=True, to='course.Session', null=True)),
            ],
            options={
                'ordering': ('-publish_dt',),
            },
            bases=(media.models.PhotosMixin, tool.models.ToolsMixin, media.models.FilesMixin, models.Model),
        ),
    ]
