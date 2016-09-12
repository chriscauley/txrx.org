# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0026_auto_20160907_1908'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoorGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('description', models.TextField(help_text=b'List all the doors this can open.')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
