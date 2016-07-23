# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0002_auto_20150614_1510'),
        ('membership', '0040_container_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='container',
            name='area',
        ),
        migrations.AddField(
            model_name='container',
            name='kind',
            field=models.CharField(default='bay', max_length=64, choices=[(b'bay', b'Bay'), (b'drawer', b'Drawer')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='container',
            name='room',
            field=models.ForeignKey(default=8, to='geo.Room'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Area',
        ),
    ]
