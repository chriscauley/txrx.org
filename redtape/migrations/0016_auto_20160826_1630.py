# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redtape', '0015_remove_document_signature_required'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documentfield',
            old_name='name',
            new_name='label',
        ),
        migrations.AlterField(
            model_name='documentfield',
            name='input_type',
            field=models.CharField(max_length=64, choices=[(b'text', b'Text'), (b'number', b'Number'), (b'phone', b'Phone'), (b'email', b'Email'), (b'header', b'Design Element (non-input)'), (b'select', b'Select'), (b'signature', b'Sign Your Name'), (b'checkbox', b'Checkbox')]),
        ),
    ]
