# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


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
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='room',
            name='location',
            field=models.ForeignKey(to='geo.Location'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='room',
            name='roomgroup',
            field=models.ForeignKey(blank=True, to='geo.RoomGroup', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='room',
            unique_together=set([('name', 'location')]),
        ),
        migrations.AddField(
            model_name='location',
            name='city',
            field=models.ForeignKey(default=1, to='geo.City'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='parent',
            field=models.ForeignKey(blank=True, to='geo.Location', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dxfentity',
            name='room',
            field=models.ForeignKey(blank=True, to='geo.Room', null=True),
            preserve_default=True,
        ),
    ]
