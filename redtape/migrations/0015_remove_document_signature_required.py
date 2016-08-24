# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redtape', '0014_remove_signature_signature'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='signature_required',
        ),
    ]
