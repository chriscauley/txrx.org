# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='usermembership',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='unsubscribelink',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='survey',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proposal',
            name='meeting_minutes',
            field=models.ForeignKey(to='membership.MeetingMinutes'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proposal',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='officer',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='membershiprate',
            name='membership',
            field=models.ForeignKey(to='membership.Membership'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='membershipfeature',
            name='feature',
            field=models.ForeignKey(to='membership.Feature'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='membershipfeature',
            name='membership',
            field=models.ForeignKey(to='membership.Membership'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='membership',
            name='membershipgroup',
            field=models.ForeignKey(blank=True, to='membership.MembershipGroup', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meetingminutes',
            name='inactive_present',
            field=models.ManyToManyField(related_name='meetings_inactive', null=True, to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meetingminutes',
            name='nonvoters_present',
            field=models.ManyToManyField(related_name='+', null=True, to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meetingminutes',
            name='voters_present',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='limitedaccesskey',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
