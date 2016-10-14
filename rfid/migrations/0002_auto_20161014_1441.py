# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def move_rfids(apps,schema_editor):
    rfid_old = apps.get_model('user','rfid')
    rfid_new = apps.get_model('rfid','rfid')
    print "%s old rfids"%rfid_old.objects.all().count()
    for rfid in rfid_old.objects.all():
        rfid_new.objects.get_or_create(
            user=rfid.user,
            number=rfid.number,
            added=rfid.added
        )
    print "%s new rfids"%rfid_new.objects.all().count()

class Migration(migrations.Migration):

    dependencies = [
        ('rfid', '0001_initial'),
        ('user', '0003_user_is_volunteer'),
    ]

    operations = [
        migrations.RunPython(move_rfids,lambda a,b: None)
    ]
