# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('membership', '0006_auto_20161028_1121'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionBuddy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('paid_until', models.DateTimeField(null=True, blank=True)),
                ('level_override', models.ForeignKey(blank=True, to='membership.Level', null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='subscription',
            name='amount',
            field=models.DecimalField(default=0, help_text=b'If zero, this membership will always be active until deleted.', max_digits=30, decimal_places=2),
        ),
        migrations.AddField(
            model_name='subscriptionbuddy',
            name='subscription',
            field=models.ForeignKey(to='membership.Subscription'),
        ),
        migrations.AddField(
            model_name='subscriptionbuddy',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
