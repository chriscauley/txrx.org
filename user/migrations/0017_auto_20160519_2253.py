# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_rfid_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='paypal_email',
            field=models.EmailField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(unique=True, max_length=255, verbose_name='email address'),
        ),
    ]
