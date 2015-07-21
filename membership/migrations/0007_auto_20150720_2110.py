# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('membership', '0006_membershiprate_cost'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipPurchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transaction_id', models.CharField(max_length=20, null=True, blank=True)),
                ('old_expiration_date', models.DateField(null=True, blank=True)),
                ('notes', models.CharField(max_length=128, null=True, blank=True)),
                ('membershipproduct', models.ForeignKey(blank=True, to='membership.MembershipProduct', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='membershiprate',
            name='membership',
        ),
        migrations.DeleteModel(
            name='MembershipRate',
        ),
        migrations.AddField(
            model_name='usermembership',
            name='membership_expiration',
            field=models.DateField(default=datetime.date.today),
            preserve_default=True,
        ),
    ]
