# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_auto_20150509_1700'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='toolsmixin_ptr',
        ),
        migrations.AddField(
            model_name='course',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=1, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
