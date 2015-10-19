# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('content', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Signature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_typed', models.CharField(max_length=64)),
                ('name_typed', models.CharField(max_length=128)),
                ('signature', models.ImageField(upload_to=b'signatures/%m-%d-%y')),
                ('date', models.DateField(auto_now_add=True)),
                ('document', models.ForeignKey(to='redtape.Document')),
            ],
        ),
    ]
