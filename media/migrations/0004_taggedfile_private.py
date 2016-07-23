# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0003_auto_20160320_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='taggedfile',
            name='private',
            field=models.BooleanField(default=False, help_text=b'Files will not appear until after the user has completed a class.'),
        ),
    ]
