# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0018_remove_enrollment_old_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='private',
            field=models.BooleanField(default=False, help_text=b'Private classes cannot be signed up for and do not appear on the session page unless the user is manually enrolled. It will appear on calendar but it will be marked in red.'),
        ),
    ]
