# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0002_auto_20150614_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagramphoto',
            name='instagram_tags',
            field=models.ManyToManyField(to='instagram.InstagramTag', blank=True),
        ),
    ]
