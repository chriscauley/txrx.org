# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0020_auto_20150918_1737'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionFlag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.CharField(max_length=32, choices=[(b'recurring_payment_skipped', b'PayPal Skipped'), (b'recurring_payment_failed', b'PayPal Failed Recurring'), (b'recurring_payment_suspended', b'PayPal Suspended'), (b'subscr_failed', b'PayPal Failed Subscription'), (b'subscr_eot', b'PayPal End of Term')])),
                ('status', models.CharField(default=b'new', max_length=32, choices=[(b'new', b'New'), (b'first_warning', b'Warned Once'), (b'second_warning', b'Warned Twice'), (b'final_warning', b'Canceled'), (b'resolved', b'Resolved'), (b'paid', b'Paid')])),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('emailed', models.DateTimeField(null=True, blank=True)),
                ('subscription', models.ForeignKey(to='membership.Subscription')),
            ],
        ),
        migrations.RemoveField(
            model_name='userflag',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='userflag',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserFlag',
        ),
    ]
