# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redtape', '0009_auto_20160308_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='editable',
            field=models.BooleanField(default=True, help_text=b'After submitting the document can the creator edit it?'),
        ),
    ]
