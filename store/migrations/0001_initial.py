# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import media.models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_session_overbook'),
        ('drop', '0001_initial'),
        ('tool', '0005_toolcheckoutitemgroup'),
    ]

    operations = [
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
            ],
            options={
                'ordering': ('name',),
            },
            bases=(media.models.PhotosMixin, 'drop.product'),
        ),
        migrations.CreateModel(
            name='CourseCheckout',
            fields=[
                ('product_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='drop.Product')),
                ('course', models.ForeignKey(to='course.Course')),
            ],
            options={
                'abstract': False,
            },
            bases=(media.models.PhotosMixin, 'drop.product'),
        ),
        migrations.CreateModel(
            name='ToolConsumableGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('consumables', models.ManyToManyField(to='store.Consumable')),
                ('tools', models.ManyToManyField(to='tool.Tool')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
