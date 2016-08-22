# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redtape', '0011_auto_20160723_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signature',
            name='signature',
            field=models.CharField(help_text=b'You signature must start with a /s/. For example enter "/s/John Hancock" without the quotes.', max_length=128, null=True, blank=True),
        ),
    ]
