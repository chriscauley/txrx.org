# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='from_email',
            field=models.EmailField(max_length=254, verbose_name=b'Email'),
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(help_text=b'Use if desired email is not in a user account. THIS FIELD DOES NOTHING IF THERE IS A USER', max_length=254, null=True, blank=True),
        ),
    ]
