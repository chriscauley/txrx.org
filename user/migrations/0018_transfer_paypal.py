# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def transfer_paypal(apps,schema_editor):
    User = apps.get_model('user','user')
    for u in User.objects.filter(usermembership__paypal_email__isnull=False):
        print u.usermembership.paypal_email
        u.paypal_email = u.usermembership.paypal_email
        u.save()

class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_auto_20160519_2253'),
        ('membership', '0038_level_permission_description'),
    ]

    operations = [
        migrations.RunPython(transfer_paypal)
    ]
