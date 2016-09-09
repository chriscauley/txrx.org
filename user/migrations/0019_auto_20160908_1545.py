# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_transfer_paypal'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='headshot',
            field=models.FileField(upload_to=b'%Y%m', storage=django.core.files.storage.FileSystemStorage(base_url=b'/staff_images', location=b'/home/chriscauley/txrx.org/main/staff_images'), max_length=200, blank=True, null=True, verbose_name=b'Head Shot'),
        ),
        migrations.AddField(
            model_name='user',
            name='id_photo_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
