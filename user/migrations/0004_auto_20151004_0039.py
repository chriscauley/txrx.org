# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def transfer_level(apps,schema_editor):
    User = apps.get_model('user','user')
    for user in User.objects.all():
        user.level = user.usermembership.level
        user.save()
        u = User.objects.get(pk=user.pk)
        assert(u.level==u.usermembership.level)
    print "miiiiiiiigreater"

class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_level'),
    ]

    operations = [
        migrations.RunPython(transfer_level)
    ]
