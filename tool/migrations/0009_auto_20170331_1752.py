# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-03-31 17:52
from __future__ import unicode_literals

from django.db import migrations

def move_status_over(apps, schema_editor):
    for m in ['course.courseenrollment','course.enrollment','redtape.signature','event.rsvp']:
        model = apps.get_model(m)
        for obj in model.objects.all():
            if obj.completed:
                obj.status = "completed"
            if obj.failed:
                obj.status = "failed"
            obj.status_changed = obj.completed or obj.failed or obj.datetime
            obj.save()
        assert(model.objects.filter(status="failed",failed__isnull=True).count() == 0)
        assert(model.objects.filter(status="completed",completed__isnull=True).count() == 0)
        assert(model.objects.filter(status="new",completed__isnull=False).count() == 0)
        assert(model.objects.filter(status="new",failed__isnull=False).count() == 0)

class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0008_auto_20170331_1746'),
        ('redtape', '0025_auto_20170331_1831'),
        ('event', '0011_auto_20170331_1831'),
        ('course', '0011_auto_20170331_1826'),
    ]

    operations = [
        migrations.RunPython(move_status_over,lambda a,b: None),
    ]