# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tool', '0006_auto_20151007_1606'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCriterion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('source', models.CharField(max_length=16, choices=[(b'course', b'Course completion'), (b'checkout', b'Checkout')])),
                ('criterion', models.ForeignKey(to='tool.Criterion')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
