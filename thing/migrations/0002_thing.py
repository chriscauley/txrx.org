# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wmd.models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0001_initial'),
        ('course', '0002_course_coursecompletion_coursesubscription_enrollment_evaluation_session_subject_term'),
        ('thing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Thing',
            fields=[
                ('toolsmixin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='tool.ToolsMixin')),
                ('title', models.CharField(max_length=128)),
                ('description', wmd.models.MarkDownField(null=True, blank=True)),
                ('publish_dt', models.DateTimeField(auto_now_add=True)),
                ('featured', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=False)),
                ('parent_link', models.URLField(null=True, blank=True)),
                ('materials', models.ManyToManyField(to='thing.Material', null=True, blank=True)),
                ('parent', models.ForeignKey(blank=True, to='thing.Thing', null=True)),
                ('session', models.ForeignKey(blank=True, to='course.Session', null=True)),
            ],
            options={
                'ordering': ('-publish_dt',),
            },
            bases=('tool.toolsmixin', models.Model),
        ),
    ]
