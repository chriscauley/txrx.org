# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsignature.fields


class Migration(migrations.Migration):

    dependencies = [
        ('redtape', '0008_auto_20160220_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signature',
            name='signature',
            field=jsignature.fields.JSignatureField(null=True, blank=True),
        ),
    ]
