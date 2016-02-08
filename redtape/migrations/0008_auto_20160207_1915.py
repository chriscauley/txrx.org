# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('redtape', '0007_documentfield_choices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentfield',
            name='choices',
            field=models.TextField(help_text=b'Javascript array object for choice fields.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='documentfield',
            name='input_type',
            field=models.CharField(max_length=64, choices=[(b'text', b'Text'), (b'number', b'Number'), (b'phone', b'Phone'), (b'email', b'Email'), (b'header', b'Design Element (non-input)'), (b'select', b'Select')]),
        ),
    ]
