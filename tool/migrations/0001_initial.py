# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wmd.models


class Migration(migrations.Migration):

    dependencies = [
        ('thing', '0001_initial'),
        ('geo', '0002_auto_20150509_1700'),
        ('contenttypes', '0001_initial'),
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=99999)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(null=True, blank=True)),
                ('photo', models.ForeignKey(blank=True, to='media.Photo', null=True)),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaggedTool',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.IntegerField()),
                ('order', models.IntegerField(default=9999)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
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
                ('lab', models.ForeignKey(to='tool.Lab')),
                ('materials', models.ManyToManyField(to='thing.Material', null=True, blank=True)),
                ('room', models.ForeignKey(blank=True, to='geo.Room', null=True)),
            ],
            options={
                'ordering': ('lab', 'order'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ToolCertification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('safety', models.BooleanField(default=False)),
                ('waiver', models.BooleanField(default=False)),
                ('room', models.ForeignKey(to='geo.Room')),
                ('tool', models.ForeignKey(to='tool.Tool')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ToolLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=99999)),
                ('title', models.CharField(max_length=64)),
                ('url', models.URLField()),
                ('tool', models.ForeignKey(to='tool.Tool')),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ToolsMixin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='taggedtool',
            name='tool',
            field=models.ForeignKey(to='tool.Tool'),
            preserve_default=True,
        ),
    ]
