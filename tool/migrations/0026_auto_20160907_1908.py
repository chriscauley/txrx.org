# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import datetime

def expire_safety_training(apps,schema_editor):
    ucs = apps.get_model('tool','usercriterion').objects.filter(criterion_id=settings.SAFETY_CRITERION_ID)
    ucs = ucs.filter(content_type__model='subscription')
    Enrollment = apps.get_model('course','enrollment')
    safety_course = apps.get_model('course','course').objects.get(name__icontains='safety')
    total = len(ucs)
    for uc in ucs:
        enrollments = Enrollment.objects.filter(user=uc.user,session__course=safety_course,completed__isnull=False)
        if enrollments:
            uc.content_object = enrollments[0]
            uc.save()
            print "Saved! ",uc.user," ",uc.criterion
        else:
            uc.expires=datetime.datetime.now()+datetime.timedelta(90)
            print "Failed! ",uc.user.username," ",uc.criterion.id
            uc.save()
    print total,'  ',apps.get_model('tool','usercriterion').objects.filter(expires__isnull=False).count()

class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0025_usercriterion_expires'),
    ]

    operations = [
        migrations.RunPython(expire_safety_training,lambda a,b:None)
    ]
