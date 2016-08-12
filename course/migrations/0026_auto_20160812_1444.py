# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def start_in_to_classroomtime(apps,schema_editor):
    Course = apps.get_model('course','course')
    CourseRoomTime = apps.get_model('course','courseroomtime')
    print ''
    courses = Course.objects.filter(start_in__isnull=False)
    print "Migrating %s courses"%(courses.count())
    for course in courses:
        defaults = {'hours_at': 0.5}
        crt,new = CourseRoomTime.objects.get_or_create(
            course = course,
            room = course.start_in,
            defaults=defaults
        )

def classroomtime_to_start_in(apps,schema_editor):
    Course = apps.get_model('course','course')
    CourseRoomTime = apps.get_model('course','courseroomtime')
    #! not actually reversing cause I'm lazy

class Migration(migrations.Migration):

    dependencies = [
        ('course', '0025_auto_20160708_1433'),
    ]

    operations = [
        migrations.RunPython(start_in_to_classroomtime,classroomtime_to_start_in)
    ]
