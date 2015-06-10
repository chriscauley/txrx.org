# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thing', '0004_auto_20150609_2057'),
        ('course', '0004_auto_20150609_2057'),
        ('tool', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ToolsMixin',
        ),
    ]
