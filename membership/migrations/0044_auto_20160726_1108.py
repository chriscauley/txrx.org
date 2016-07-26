# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.db import migrations, models

def user_to_subscription(apps,schema_migrations):
    #Container = apps.get_model("membership","container")
    from membership.models import Container
    for container in Container.objects.filter(user__isnull=False):
        for subscription in container.user.subscription_set.all():
            if subscription.canceled and subscription.canceled < datetime.datetime.now():
                print "skips!"
                continue
            if container.subscription:
                print container," already has subscription %s %s"%(subscription, container.subscription)
            if subscription.product.level > 20:
                container.subscription = subscription
                container.save()
        if container.subscription:
            container.user = None  
            container.save()
        else:
            print "No subscription for %s"%container  

def subscirpiton_to_user(apps,schema_migrations):
    for container in apps.get_model("membership","contianer").objects.filter(subscription__isnull=False):
        container.user = container.subscripiton.user
        container.subscription = False
        container.save()

class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0043_auto_20160726_1021'),
    ]

    operations = [
        migrations.RunPython(user_to_subscription,lambda *args:None)
    ]
