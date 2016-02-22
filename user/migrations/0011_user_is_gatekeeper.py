# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_usernote'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_gatekeeper',
            field=models.BooleanField(default=False, help_text=b'Gatekeepers have 24/7 building access.'),
        ),
    ]
