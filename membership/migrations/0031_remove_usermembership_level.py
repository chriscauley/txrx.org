# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0030_auto_20151003_2114'),
        ('user', '0004_auto_20151004_0039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermembership',
            name='level',
        ),
    ]
