# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-02-21 13:29
from __future__ import unicode_literals

from django.db import migrations
from lablackey.contenttypes import get_contenttype

def move_to_follow(apps,schema_editor):
    NotifyCourse = apps.get_model("notify","NotifyCourse")
    Follow = apps.get_model("notify","Follow")
    if not NotifyCourse.objects.all():
        return
    course_ct_id = get_contenttype("course.course").id
    print NotifyCourse.objects.count(),' ',Follow.objects.count()
    for nc in NotifyCourse.objects.all():
        Follow.objects.get_or_create(
            user=nc.user,
            content_type_id=course_ct_id,
            object_id=nc.course_id,
        )
    print NotifyCourse.objects.count(),' ',Follow.objects.count()


class Migration(migrations.Migration):

    dependencies = [
        ('notify', '0003_auto_20170221_1321'),
    ]

    operations = [
        migrations.RunPython(move_to_follow,lambda *args: None)
    ]
