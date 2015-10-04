# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0003_auto_20151003_2211'),
    ]

    operations = [
        migrations.CreateModel(
            name='Criterion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='permission',
            name='criteria',
            field=models.ManyToManyField(to='tool.Criterion'),
        ),
    ]
