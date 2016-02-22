# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0008_auto_20150903_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingminutes',
            name='inactive_present',
            field=models.ManyToManyField(related_name='meetings_inactive', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='meetingminutes',
            name='nonvoters_present',
            field=models.ManyToManyField(related_name='+', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='meetingminutes',
            name='voters_present',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usermembership',
            name='paypal_email',
            field=models.EmailField(help_text=b'Leave blank if this is the same as your email address above.', max_length=254, null=True, blank=True),
        ),
    ]
