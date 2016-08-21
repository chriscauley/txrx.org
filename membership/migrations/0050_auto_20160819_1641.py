# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0049_container_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='status',
            field=models.CharField(default=b'used', help_text=b'Automatically set when changes are made to subscription or container via admin.', max_length=16, choices=[(b'used', b'Used'), (b'staff', b'Staff'), (b'canceled', b'Needs Email'), (b'emailed', b'Emailed'), (b'maintenance', b'Maintenance'), (b'open', b'Open')]),
        ),
    ]
