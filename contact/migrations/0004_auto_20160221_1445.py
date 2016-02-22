# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0003_message_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='marked_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='message',
            name='read_count',
            field=models.IntegerField(default=0),
        ),
    ]
