# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def remove_product(apps,schema_editor):
    for subscription in apps.get_model("membership","subscription").objects.all():
        subscription.level = subscription.product.level
        subscription.months = subscription.product.months
        subscription.save()

class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0003_subscription_months'),
    ]

    operations = [
        migrations.RunPython(remove_product,lambda a,b:None)
    ]
