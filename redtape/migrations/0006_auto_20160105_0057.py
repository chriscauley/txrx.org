# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('redtape', '0005_auto_20160103_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('slug', models.CharField(help_text=b'For fields with the same name', max_length=64, null=True, blank=True)),
                ('order', models.IntegerField(default=999)),
                ('input_type', models.CharField(max_length=64, choices=[(b'text', b'Text'), (b'number', b'Number'), (b'phone', b'Phone'), (b'email', b'Email'), (b'header', b'Design Element (non-input)')])),
                ('required', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.AddField(
            model_name='document',
            name='signature_required',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='signature',
            name='data',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='signature',
            name='date_typed',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Type Todays Date', blank=True),
        ),
        migrations.AlterField(
            model_name='signature',
            name='name_typed',
            field=models.CharField(max_length=128, null=True, verbose_name=b'Type Your Name', blank=True),
        ),
        migrations.AlterField(
            model_name='signature',
            name='signature',
            field=models.ImageField(null=True, upload_to=b'signatures/%m-%d-%y', blank=True),
        ),
        migrations.AddField(
            model_name='documentfield',
            name='document',
            field=models.ForeignKey(to='redtape.Document'),
        ),
    ]
