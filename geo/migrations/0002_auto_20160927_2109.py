# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0001_initial'),
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomgroup',
            name='fill',
            field=models.ForeignKey(blank=True, to='media.Photo', null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='location',
            field=models.ForeignKey(to='geo.Location'),
        ),
        migrations.AddField(
            model_name='room',
            name='roomgroup',
            field=models.ForeignKey(blank=True, to='geo.RoomGroup', null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='city',
            field=models.ForeignKey(default=1, to='geo.City'),
        ),
        migrations.AddField(
            model_name='location',
            name='parent',
            field=models.ForeignKey(blank=True, to='geo.Location', null=True),
        ),
        migrations.AddField(
            model_name='dxfentity',
            name='room',
            field=models.ForeignKey(blank=True, to='geo.Room', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='room',
            unique_together=set([('name', 'location')]),
        ),
    ]
