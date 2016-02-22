# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0011_criterion_supervisors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='criterion',
            name='supervisors',
        ),
    ]
