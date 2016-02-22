# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BulkEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=128)),
                ('body', models.TextField()),
                ('send_on_save', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BulkEmailRecipient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75)),
                ('name', models.CharField(max_length=64)),
                ('file1', models.FileField(null=True, upload_to=b'bulkemail', blank=True)),
                ('file2', models.FileField(null=True, upload_to=b'bulkemail', blank=True)),
                ('sent', models.DateTimeField(null=True, blank=True)),
                ('bulkemail', models.ForeignKey(to='misc.BulkEmail')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
