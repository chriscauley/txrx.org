# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def move_rfids(apps,schema_editor):
    User = apps.get_model("user","User")
    RFIDCard = apps.get_model("user","RFIDCard")
    for user in User.objects.filter(rfid__isnull=False).exclude(rfid=""):
        card,new = RFIDCard.objects.get_or_create(user=user,number=user.rfid)
        if new:
            print "%s created!"%card

class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_rfidcard'),
    ]

    operations = [
        migrations.RunPython(move_rfids)
    ]
