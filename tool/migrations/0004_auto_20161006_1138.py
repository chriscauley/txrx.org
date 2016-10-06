# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0003_checkoutitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkoutitem',
            name='room',
            field=models.ForeignKey(help_text=b'Only rooms marked "has checkoutitems" appear here', to='geo.Room'),
        ),
    ]
