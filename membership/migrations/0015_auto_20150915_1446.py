# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0014_auto_20150913_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userflag',
            name='reason',
            field=models.CharField(max_length=32, choices=[(b'paypal_skipped', b'PayPal Skipped')]),
        ),
        migrations.AlterField(
            model_name='userflag',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
