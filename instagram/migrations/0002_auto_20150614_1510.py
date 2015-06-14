# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('instagram', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramuser',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='instagramphoto',
            name='instagram_location',
            field=models.ForeignKey(blank=True, to='instagram.InstagramLocation', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='instagramphoto',
            name='instagram_tags',
            field=models.ManyToManyField(to='instagram.InstagramTag', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='instagramphoto',
            name='instagram_user',
            field=models.ForeignKey(blank=True, to='instagram.InstagramUser', null=True),
            preserve_default=True,
        ),
    ]
