# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import redtape.models


class Migration(migrations.Migration):

    dependencies = [
        ('redtape', '0012_auto_20160822_1423'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signature',
            name='date_typed',
        ),
        migrations.RemoveField(
            model_name='signature',
            name='name_typed',
        ),
        migrations.AlterField(
            model_name='documentfield',
            name='input_type',
            field=models.CharField(max_length=64, choices=[(b'text', b'Text'), (b'number', b'Number'), (b'phone', b'Phone'), (b'email', b'Email'), (b'header', b'Design Element (non-input)'), (b'select', b'Select'), (b'signature', b'Sign Your Name')]),
        ),
        migrations.AlterField(
            model_name='signature',
            name='signature',
            field=models.CharField(blank=True, max_length=128, null=True, help_text=b'You signature must start with a /s/. For example enter "/s/John Hancock" without the quotes.', validators=[redtape.models.signature_validator]),
        ),
    ]
