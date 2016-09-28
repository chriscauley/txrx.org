# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import media.models


class Migration(migrations.Migration):

    dependencies = [
        ('drop', '0004_auto_20160908_1023'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('order', models.FloatField(default=0)),
                ('level', models.IntegerField(default=0)),
                ('parent', models.ForeignKey(blank=True, to='store.Category', null=True)),
            ],
            options={
                'ordering': ('order',),
                'verbose_name_plural': 'Categories',
            },
            bases=(media.models.PhotosMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Consumable',
            fields=[
                ('product_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='drop.Product')),
                ('part_number', models.CharField(max_length=32, null=True, blank=True)),
                ('part_style', models.CharField(max_length=32, null=True, blank=True)),
                ('purchase_url', models.URLField(max_length=1024, null=True, blank=True)),
                ('purchase_url2', models.URLField(max_length=1024, null=True, blank=True)),
                ('in_stock', models.IntegerField(help_text=b'Leave blank and this fill always show as in stock.', null=True, blank=True)),
                ('purchase_quantity', models.IntegerField(default=1, help_text=b'Amount purchased at a time. Used to make the quick refill process.')),
                ('categories', models.ManyToManyField(to='store.Category')),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(media.models.PhotosMixin, 'drop.product'),
        ),
        migrations.CreateModel(
            name='TaggedConsumable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.IntegerField()),
                ('order', models.IntegerField(default=9999)),
                ('consumable', models.ForeignKey(to='store.Consumable')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
    ]
