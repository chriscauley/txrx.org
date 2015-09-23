# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0026_auto_20150923_1215'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membershipfeature',
            old_name='membership',
            new_name='level',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='membership',
            new_name='level',
        ),
        migrations.RenameField(
            model_name='usermembership',
            old_name='membership',
            new_name='level',
        ),
    ]
