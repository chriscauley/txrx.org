# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('membership', '0015_auto_20150915_1446'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='container',
        ),
        migrations.RemoveField(
            model_name='usermembership',
            name='container',
        ),
        migrations.AddField(
            model_name='container',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userflag',
            name='reason',
            field=models.CharField(max_length=32, choices=[(b'recurring_payment_skipped', b'PayPal Skipped'), (b'recurring_payment_failed', b'PayPal Failed Recurring'), (b'recurring_payment_suspended', b'PayPal Suspended'), (b'subscr_failed', b'PayPal Failed Subscription'), (b'subscr_eot', b'PayPal End of Term')]),
        ),
    ]
