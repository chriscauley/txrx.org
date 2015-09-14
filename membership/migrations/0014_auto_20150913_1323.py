# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('membership', '0013_auto_20150908_1859'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFlag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.IntegerField()),
                ('reason', models.CharField(max_length=32, choices=[(b'payment_skipped', b'PaymentSkipped')])),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='usermembership',
            name='flagged',
        ),
    ]
