# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def transfer_orientation_status(apps,schema_editor):
    User = apps.get_model('user','user')
    for user in User.objects.all():
        user.orientation_status = user.usermembership.orientation_status
        user.save()
        u = User.objects.get(pk=user.pk)
        assert(u.orientation_status==u.usermembership.orientation_status)
    print "miiiiiiiigreat!"

class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_user_orientation_status'),
    ]

    operations = [
        migrations.RunPython(transfer_orientation_status)
    ]
