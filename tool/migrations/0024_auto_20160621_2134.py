# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0039_remove_usermembership_paypal_email'),
        ('tool', '0023_schedule_scheduleday'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermissionSchedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('levels', models.ManyToManyField(to='membership.Level')),
                ('permission', models.ForeignKey(to='tool.Permission')),
                ('schedule', models.ForeignKey(to='tool.Schedule')),
            ],
        ),
        migrations.AlterModelOptions(
            name='scheduleday',
            options={'ordering': ('dow',)},
        ),
    ]
