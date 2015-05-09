# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0002_auto_20150509_1700'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0002_course_coursecompletion_coursesubscription_enrollment_evaluation_session_subject_term'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='evaluation',
            name='enrollment',
            field=models.ForeignKey(to='course.Enrollment', unique=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='evaluation',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enrollment',
            name='session',
            field=models.ForeignKey(to='course.Session'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enrollment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coursesubscription',
            name='course',
            field=models.ForeignKey(to='course.Course'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coursesubscription',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coursecompletion',
            name='course',
            field=models.ForeignKey(to='course.Course'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coursecompletion',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='room',
            field=models.ForeignKey(to='geo.Room'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='start_in',
            field=models.ForeignKey(related_name='starting_courses', blank=True, to='geo.Room', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='subjects',
            field=models.ManyToManyField(to='course.Subject'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classtime',
            name='session',
            field=models.ForeignKey(to='course.Session'),
            preserve_default=True,
        ),
    ]
