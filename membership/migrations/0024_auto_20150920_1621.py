# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def transaction_check(apps,schema_editor):
    Status = apps.get_model('membership','Status')
    for status in Status.objects.filter(paypalipn__isnull=False):
        extra = Status.objects.filter(transaction_id=status.paypalipn.txn_id).exclude(pk=status.pk)
        if extra:
            print "deleted status for %s"%status.subscription.user.username
            status.delete()
            continue
        status.transaction_id = status.paypalipn.txn_id
        status.save()

class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0023_auto_20150920_1621'),
    ]

    operations = [
        migrations.RunPython(transaction_check)
    ]
