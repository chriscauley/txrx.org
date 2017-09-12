# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-09-11 14:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_event_orientation_required'),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursecheckout',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='event.Event'),
        ),
    ]