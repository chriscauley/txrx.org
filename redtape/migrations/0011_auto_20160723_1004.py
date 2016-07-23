# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redtape', '0010_document_editable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='editable',
            field=models.BooleanField(default=True, help_text=b'After submitting the document can the creator edit it?If false a new document will be created everytime they submit the document.'),
        ),
    ]
