# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0002_auto_20150614_1510'),
        ('tool', '0002_auto_20150908_1209'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('safety', models.BooleanField(default=True)),
                ('room', models.ForeignKey(to='geo.Room')),
                ('tools', models.ManyToManyField(to='tool.Tool')),
            ],
        ),
        migrations.RemoveField(
            model_name='toolcertification',
            name='room',
        ),
        migrations.RemoveField(
            model_name='toolcertification',
            name='tool',
        ),
        migrations.DeleteModel(
            name='ToolCertification',
        ),
    ]
