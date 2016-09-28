# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0002_auto_20160927_2109'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='enrollment',
            field=models.OneToOneField(to='course.Enrollment'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='session',
            field=models.ForeignKey(to='course.Session'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='coursesubscription',
            name='course',
            field=models.ForeignKey(to='course.Course'),
        ),
        migrations.AddField(
            model_name='coursesubscription',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='courseroomtime',
            name='course',
            field=models.ForeignKey(to='course.Course'),
        ),
        migrations.AddField(
            model_name='courseroomtime',
            name='room',
            field=models.ForeignKey(to='geo.Room'),
        ),
        migrations.AddField(
            model_name='course',
            name='room',
            field=models.ForeignKey(to='geo.Room'),
        ),
        migrations.AddField(
            model_name='course',
            name='subjects',
            field=models.ManyToManyField(to='course.Subject'),
        ),
        migrations.AddField(
            model_name='classtime',
            name='session',
            field=models.ForeignKey(to='course.Session'),
        ),
    ]
