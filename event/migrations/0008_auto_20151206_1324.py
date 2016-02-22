# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0002_auto_20150614_1510'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('event', '0007_auto_20151105_1535'),
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
                ('room', models.ForeignKey(to='geo.Room')),
            ],
            options={
                'ordering': ('room__name',),
            },
        ),
        migrations.AddField(
            model_name='checkin',
            name='checkinpoint',
            field=models.ForeignKey(to='event.CheckInPoint'),
        ),
        migrations.AddField(
            model_name='checkin',
            name='content_type',
            field=models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='checkin',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
