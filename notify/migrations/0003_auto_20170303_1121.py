# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-03-03 11:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import lablackey.unrest


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notify', '0002_auto_20160927_2109'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField()),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-datetime',),
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('emailed', models.DateTimeField(blank=True, null=True)),
                ('read', models.DateTimeField(blank=True, null=True)),
                ('message', models.CharField(max_length=512)),
                ('data', jsonfield.fields.JSONField(blank=True, default=dict)),
                ('url', models.CharField(blank=True, max_length=256, null=True)),
                ('relationship', models.CharField(blank=True, max_length=32, null=True)),
                ('target_type', models.CharField(blank=True, max_length=201, null=True)),
                ('target_id', models.IntegerField(blank=True, null=True)),
                ('follow', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='notify.Follow')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-datetime',),
            },
            bases=(models.Model, lablackey.unrest.JsonMixin),
        ),
        migrations.CreateModel(
            name='NotifySettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notify_global', models.BooleanField(default=True, help_text=b'If false this wil disable all notificaitons from the site.', verbose_name=b'Global Preference')),
                ('new_comments', models.CharField(blank=True, choices=[(b'', b'Do not notify me about this'), (b'email', b'Email'), (b'sms', b'Text Message (SMS, standard rates apply)')], default=b'email', help_text=b'An email or text whenever someone replies to a comment you make on this site.', max_length=8, verbose_name=b'Comment responses')),
                ('my_classes', models.CharField(blank=True, choices=[(b'', b'Do not notify me about this'), (b'email', b'Email'), (b'sms', b'Text Message (SMS, standard rates apply)')], default=b'email', help_text=b"An email or text reminder 24 hours before a class (that you've signed up for or are teaching).", max_length=8, verbose_name=b'Class Reminders')),
                ('new_sessions', models.CharField(blank=True, choices=[(b'', b'Do not notify me about this'), (b'email', b'Email'), (b'sms', b'Text Message (SMS, standard rates apply)')], default=b'email', help_text=b"An email or text when a class you're following for has been added (only during business hours).", max_length=8, verbose_name=b'New Classes')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='notifycourse',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together=set([('user', 'content_type', 'object_id')]),
        ),
    ]
