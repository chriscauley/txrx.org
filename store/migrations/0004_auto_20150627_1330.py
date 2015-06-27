# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20150627_1323'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consumable',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='consumable',
            name='in_stock',
            field=models.IntegerField(help_text=b'Leave blank and this fill always show as in stock.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consumable',
            name='part_number',
            field=models.CharField(max_length=32, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consumable',
            name='part_style',
            field=models.CharField(max_length=32, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consumable',
            name='purchase_quantity',
            field=models.IntegerField(default=1, help_text=b'Amount purchased at a time. Used to make the quick refill process.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consumable',
            name='purchase_url',
            field=models.URLField(max_length=1024, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consumable',
            name='purchase_url2',
            field=models.URLField(max_length=1024, null=True, blank=True),
            preserve_default=True,
        ),
    ]
