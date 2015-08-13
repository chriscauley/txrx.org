# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ipn', '__first__'),
        ('membership', '0008_auto_20150725_1505'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membershipchange',
            name='old_expiration_date',
        ),
        migrations.RemoveField(
            model_name='usermembership',
            name='membership_expiration',
        ),
        migrations.AddField(
            model_name='membershipchange',
            name='action',
            field=models.CharField(default='none', max_length=16, choices=[(b'stop', b'Cancel Membership'), (b'start', b'Change Start Date'), (b'extend', b'Add Membership Time')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='membershipchange',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 12, 17, 56, 50, 915330), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='membershipchange',
            name='paypalipn',
            field=models.ForeignKey(blank=True, to='ipn.PayPalIPN', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usermembership',
            name='end',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usermembership',
            name='start',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usermembership',
            name='subscr_id',
            field=models.CharField(max_length=32, null=True, blank=True),
            preserve_default=True,
        ),
    ]
