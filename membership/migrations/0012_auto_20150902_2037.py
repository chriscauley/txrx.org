# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ipn', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('membership', '0011_membershipchange_subscr_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledPayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(default=0, max_digits=30, decimal_places=2)),
                ('due_date', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(default=0, max_digits=30, decimal_places=2)),
                ('datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('notes', models.CharField(max_length=128, null=True, blank=True)),
                ('payment_method', models.CharField(default=b'cash', max_length=16, choices=[(b'paypal', b'PayPalIPN'), (b'cash', b'Cash'), (b'adjustment', b'Adjustment'), (b'refund', b'Refund'), (b'legacy', b'Legacy (PayPal)')])),
                ('paypalipn', models.ForeignKey(blank=True, to='ipn.PayPalIPN', null=True)),
            ],
            options={
                'ordering': ('datetime',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subscr_id', models.CharField(max_length=20, null=True, blank=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('cancelled', models.DateTimeField(null=True, blank=True)),
                ('amount', models.DecimalField(default=0, max_digits=30, decimal_places=2)),
                ('owed', models.DecimalField(default=0, max_digits=30, decimal_places=2)),
                ('product', models.ForeignKey(blank=True, to='membership.MembershipProduct', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='membershipchange',
            name='membershipproduct',
        ),
        migrations.RemoveField(
            model_name='membershipchange',
            name='paypalipn',
        ),
        migrations.RemoveField(
            model_name='membershipchange',
            name='user',
        ),
        migrations.DeleteModel(
            name='MembershipChange',
        ),
        migrations.AddField(
            model_name='status',
            name='subscription',
            field=models.ForeignKey(to='membership.Subscription'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='scheduledpayment',
            name='subscription',
            field=models.ForeignKey(to='membership.Subscription'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='usermembership',
            name='subscr_id',
        ),
        migrations.AddField(
            model_name='usermembership',
            name='flagged',
            field=models.CharField(max_length=16, null=True, blank=True),
            preserve_default=True,
        ),
    ]
