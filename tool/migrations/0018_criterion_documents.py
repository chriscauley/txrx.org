# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('redtape', '0004_auto_20151027_1200'),
        ('tool', '0017_auto_20151026_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='criterion',
            name='documents',
            field=models.ManyToManyField(to='redtape.Document', blank=True),
        ),
    ]
