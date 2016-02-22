# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0014_auto_20151010_1542'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('color', models.CharField(max_length=32)),
                ('column', models.IntegerField(choices=[(0, b'left'), (1, b'right')])),
                ('row', models.IntegerField()),
            ],
            options={
                'ordering': ('column', 'row'),
            },
        ),
        migrations.AlterModelOptions(
            name='permission',
            options={'ordering': ('group', 'order')},
        ),
        migrations.AddField(
            model_name='permission',
            name='group',
            field=models.ForeignKey(blank=True, to='tool.Group', null=True),
        ),
    ]
