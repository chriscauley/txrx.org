# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0012_auto_20150908_1634'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('kind', models.CharField(max_length=64, choices=[(b'bay', b'Bay'), (b'drawer', b'Drawer')])),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
                ('area', models.ForeignKey(to='membership.Area')),
            ],
            options={
                'ordering': ('number',),
            },
        ),
        migrations.AddField(
            model_name='subscription',
            name='container',
            field=models.ForeignKey(blank=True, to='membership.Container', null=True),
        ),
        migrations.AddField(
            model_name='usermembership',
            name='container',
            field=models.ForeignKey(blank=True, to='membership.Container', null=True),
        ),
    ]
