# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('membership', '0007_auto_20150720_2110'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transaction_id', models.CharField(max_length=20, null=True, blank=True)),
                ('old_expiration_date', models.DateField(null=True, blank=True)),
                ('notes', models.CharField(max_length=128, null=True, blank=True)),
                ('payment_method', models.CharField(default=b'admin', max_length=16, choices=[(b'paypal', b'PayPalIPN'), (b'admin', b'Admin (manually entered)')])),
                ('membershipproduct', models.ForeignKey(blank=True, to='membership.MembershipProduct', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='membershippurchase',
            name='membershipproduct',
        ),
        migrations.RemoveField(
            model_name='membershippurchase',
            name='user',
        ),
        migrations.DeleteModel(
            name='MembershipPurchase',
        ),
    ]
