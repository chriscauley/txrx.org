# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('store', '0008_auto_20160819_1641'),
    ]

    operations = [
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
