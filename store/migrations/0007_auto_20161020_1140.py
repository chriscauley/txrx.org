# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def switch_categories(apps,schema_editor):
    new_category = apps.get_model("drop","category")
    old_category = apps.get_model("store","category")
    consumable = apps.get_model("store","consumable")
    coursecheckout = apps.get_model("store","coursecheckout")
    for old in old_category.objects.all():
        parent = None
        if old.parent:
            parent,new = new_category.objects.get_or_create(name=old.parent.name)
        new_category.objects.get_or_create(name=old.name,parent=parent)
    for model in [consumable,coursecheckout]:
        for p in model.objects.all():
            for old_category in p._categories.all():
                p.categories.add(new_category.objects.get(name=old_category.name))
            p.save()
            print p.name,'\t',p.categories.count(),'\t',p.categories.count()
            if p.categories.count() != p.categories.count():
                raise Exception(p.name)

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20161020_1129'),
        ('drop', '0006_product_categories'),
    ]

    operations = [
        migrations.RunPython(switch_categories,lambda a,b:None)
    ]
