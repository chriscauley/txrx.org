# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def forwards_func(apps,schema_editor):
    ContentType = apps.get_model('contenttypes','ContentType')
    ContentType.objects.filter(model='product',app_label='membership').delete()
    ContentType.objects.filter(model='membershipproduct').update(model='product')

def backwards_func(apps,schema_editor):
    ContentType = apps.get_model('contenttypes','ContentType')
    ContentType.objects.filter(model='product',app_label='membership').update(model='product')

class Migration(migrations.Migration):
    dependencies = [
        ('shop', '__first__'),
        ('membership', '0009_auto_20150908_1209'),
    ]
    operations = [
        migrations.RunPython(forwards_func,backwards_func),
        migrations.RenameModel('MembershipProduct','Product'),
    ]
