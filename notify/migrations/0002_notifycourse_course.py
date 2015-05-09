# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notify', '0001_initial'),
        ('course', '0002_course_coursecompletion_coursesubscription_enrollment_evaluation_session_subject_term'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifycourse',
            name='course',
            field=models.ForeignKey(to='course.Course'),
            preserve_default=True,
        ),
    ]
