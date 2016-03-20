# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import crop_override.field


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0002_auto_20150614_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='landscape_crop',
            field=crop_override.field.CropOverride(upload_to=b'uploads/photos/%Y-%m', max_length=200, blank=True, help_text=b'Usages: Featured Blog Photo, Lab Photo', null=True, verbose_name=b'Landscape Crop (3:2)'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='portrait_crop',
            field=crop_override.field.CropOverride(upload_to=b'uploads/photos/%Y-%m', max_length=200, blank=True, help_text=b'Usages: None', null=True, verbose_name=b'Portrait Crop (2:3)'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='square_crop',
            field=crop_override.field.CropOverride(upload_to=b'uploads/photos/%Y-%m', max_length=200, blank=True, help_text=b'Usages: Blog Photo, Tool Photo', null=True, verbose_name=b'Square Crop (1:1)'),
        ),
    ]
