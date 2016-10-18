# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlatPagePrice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=99999)),
                ('name', models.CharField(max_length=128)),
                ('flatpage', models.ForeignKey(to='flatpages.FlatPage')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=128)),
            ],
            options={
                'ordering': ('text',),
            },
        ),
        migrations.AddField(
            model_name='flatpageprice',
            name='member_rate',
            field=models.ForeignKey(related_name='+', to='main.Rate'),
        ),
        migrations.AddField(
            model_name='flatpageprice',
            name='nonmember_rate',
            field=models.ForeignKey(related_name='+', to='main.Rate'),
        ),
    ]
