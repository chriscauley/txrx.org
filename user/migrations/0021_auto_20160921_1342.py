# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0020_user_is_shopkeeper'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='headshot',
            field=models.FileField(upload_to=b'%Y%m', storage=django.core.files.storage.FileSystemStorage(base_url=b'/staff_only/', location=b'/home/chriscauley/txrx.org/main/../.staff'), max_length=200, blank=True, null=True, verbose_name=b'Head Shot'),
        ),
    ]
