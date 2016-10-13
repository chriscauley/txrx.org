# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import media.models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20160927_2109'),
        ('drop', '0004_auto_20160908_1023'),
        ('store', '0003_auto_20161006_1304'),
    ]

    operations = [
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
    ]
