# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-04-09 22:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0013_auto_20170409_2239'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursesubscription',
            name='course',
        ),
        migrations.RemoveField(
            model_name='coursesubscription',
            name='user',
        ),
        migrations.DeleteModel(
            name='CourseSubscription',
        ),
    ]