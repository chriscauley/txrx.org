# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0045_remove_container_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='container',
            options={'ordering': ('room', 'number')},
        ),
        migrations.AlterField(
            model_name='container',
            name='kind',
            field=models.CharField(default=b'bay', max_length=64, choices=[(b'drawer', b'Drawer'), (b'table', b'Table'), (b'bay', b'Bay'), (b'studio', b'Studio')]),
        ),
    ]
