# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0002_auto_20160927_2109'),
        ('thing', '0002_auto_20160927_2109'),
        ('geo', '0002_auto_20160927_2109'),
        ('redtape', '0017_auto_20160826_1633'),
        ('media', '0002_auto_20160927_2109'),
        ('membership', '0002_auto_20160927_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercriterion',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='toollink',
            name='tool',
            field=models.ForeignKey(to='tool.Tool'),
        ),
        migrations.AddField(
            model_name='tool',
            name='lab',
            field=models.ForeignKey(to='tool.Lab'),
        ),
        migrations.AddField(
            model_name='tool',
            name='materials',
            field=models.ManyToManyField(to='thing.Material', blank=True),
        ),
        migrations.AddField(
            model_name='tool',
            name='permission',
            field=models.ForeignKey(blank=True, to='tool.Permission', null=True),
        ),
        migrations.AddField(
            model_name='tool',
            name='room',
            field=models.ForeignKey(blank=True, to='geo.Room', null=True),
        ),
        migrations.AddField(
            model_name='taggedtool',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='taggedtool',
            name='tool',
            field=models.ForeignKey(to='tool.Tool'),
        ),
        migrations.AddField(
            model_name='scheduleday',
            name='schedule',
            field=models.ForeignKey(to='tool.Schedule'),
        ),
        migrations.AddField(
            model_name='permissionschedule',
            name='levels',
            field=models.ManyToManyField(to='membership.Level'),
        ),
        migrations.AddField(
            model_name='permissionschedule',
            name='permission',
            field=models.ForeignKey(to='tool.Permission'),
        ),
        migrations.AddField(
            model_name='permissionschedule',
            name='schedule',
            field=models.ForeignKey(to='tool.Schedule'),
        ),
        migrations.AddField(
            model_name='permission',
            name='criteria',
            field=models.ManyToManyField(help_text=b'Requires all these criteria to access these tools.', to='tool.Criterion', blank=True),
        ),
        migrations.AddField(
            model_name='permission',
            name='group',
            field=models.ForeignKey(blank=True, to='tool.Group', null=True),
        ),
        migrations.AddField(
            model_name='permission',
            name='room',
            field=models.ForeignKey(to='geo.Room'),
        ),
        migrations.AddField(
            model_name='lab',
            name='photo',
            field=models.ForeignKey(blank=True, to='media.Photo', null=True),
        ),
        migrations.AddField(
            model_name='criterion',
            name='courses',
            field=models.ManyToManyField(to='course.Course', blank=True),
        ),
        migrations.AddField(
            model_name='criterion',
            name='documents',
            field=models.ManyToManyField(to='redtape.Document', blank=True),
        ),
    ]
