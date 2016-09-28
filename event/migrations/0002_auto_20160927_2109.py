# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('geo', '0002_auto_20160927_2109'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rsvp',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='eventoccurrence',
            name='event',
            field=models.ForeignKey(to='event.Event'),
        ),
        migrations.AddField(
            model_name='event',
            name='room',
            field=models.ForeignKey(blank=True, to='geo.Room', null=True),
        ),
        migrations.AddField(
            model_name='checkinpoint',
            name='room',
            field=models.ForeignKey(to='geo.Room'),
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
