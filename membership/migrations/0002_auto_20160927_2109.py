# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ipn', '0007_auto_20160219_1135'),
        ('tool', '0001_initial'),
        ('membership', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geo', '0002_auto_20160927_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermembership',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='unsubscribelink',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='survey',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subscription',
            name='product',
            field=models.ForeignKey(to='membership.Product'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='status',
            name='paypalipn',
            field=models.ForeignKey(blank=True, to='ipn.PayPalIPN', null=True),
        ),
        migrations.AddField(
            model_name='status',
            name='subscription',
            field=models.ForeignKey(to='membership.Subscription'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='meeting_minutes',
            field=models.ForeignKey(to='membership.MeetingMinutes'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='level',
            field=models.ForeignKey(to='membership.Level'),
        ),
        migrations.AddField(
            model_name='officer',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='membershipfeature',
            name='feature',
            field=models.ForeignKey(to='membership.Feature'),
        ),
        migrations.AddField(
            model_name='membershipfeature',
            name='level',
            field=models.ForeignKey(to='membership.Level'),
        ),
        migrations.AddField(
            model_name='meetingminutes',
            name='inactive_present',
            field=models.ManyToManyField(related_name='meetings_inactive', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='meetingminutes',
            name='nonvoters_present',
            field=models.ManyToManyField(related_name='_meetingminutes_nonvoters_present_+', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='meetingminutes',
            name='voters_present',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='limitedaccesskey',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='leveldoorgroupschedule',
            name='doorgroup',
            field=models.ForeignKey(to='tool.DoorGroup'),
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
        migrations.AddField(
            model_name='level',
            name='door_schedule',
            field=models.ForeignKey(related_name='+', blank=True, to='tool.Schedule', null=True),
        ),
        migrations.AddField(
            model_name='level',
            name='group',
            field=models.ForeignKey(blank=True, to='membership.Group', null=True),
        ),
        migrations.AddField(
            model_name='level',
            name='tool_schedule',
            field=models.ForeignKey(related_name='+', blank=True, to='tool.Schedule', null=True),
        ),
        migrations.AddField(
            model_name='flag',
            name='subscription',
            field=models.ForeignKey(to='membership.Subscription'),
        ),
        migrations.AddField(
            model_name='container',
            name='room',
            field=models.ForeignKey(to='geo.Room'),
        ),
        migrations.AddField(
            model_name='container',
            name='subscription',
            field=models.OneToOneField(null=True, blank=True, to='membership.Subscription'),
        ),
        migrations.AlterUniqueTogether(
            name='leveldoorgroupschedule',
            unique_together=set([('level', 'doorgroup')]),
        ),
    ]
