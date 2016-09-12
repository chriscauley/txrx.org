# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0027_doorgroup'),
        ('membership', '0051_auto_20160819_1701'),
    ]

    operations = [
        migrations.CreateModel(
            name='LevelDoorGroupSchedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('doorgroup', models.ForeignKey(to='tool.DoorGroup')),
            ],
            options={
                'ordering': ('level',),
            },
        ),
        migrations.AddField(
            model_name='level',
            name='door_schedule',
            field=models.ForeignKey(related_name='+', blank=True, to='tool.Schedule', null=True),
        ),
        migrations.AddField(
            model_name='level',
            name='tool_schedule',
            field=models.ForeignKey(related_name='+', blank=True, to='tool.Schedule', null=True),
        ),
        migrations.AddField(
            model_name='leveldoorgroupschedule',
            name='level',
            field=models.ForeignKey(to='membership.Level'),
        ),
        migrations.AddField(
            model_name='leveldoorgroupschedule',
            name='schedule',
            field=models.ForeignKey(to='tool.Schedule'),
        ),
    ]
