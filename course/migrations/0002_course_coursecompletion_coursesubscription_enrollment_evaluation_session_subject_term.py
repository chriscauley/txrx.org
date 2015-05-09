# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0001_initial'),
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('toolsmixin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='tool.ToolsMixin')),
                ('name', models.CharField(max_length=64)),
                ('active', models.BooleanField(default=True)),
                ('short_name', models.CharField(help_text=b'Used for the events page.', max_length=64, null=True, blank=True)),
                ('presentation', models.BooleanField(default=True, verbose_name=b'Evaluate Presentation')),
                ('visuals', models.BooleanField(default=True, verbose_name=b'Evaluate Visuals')),
                ('content', models.BooleanField(default=True, verbose_name=b'Evaluate Content')),
                ('reschedule_on', models.DateField(default=datetime.date.today, help_text=b"The dashboard (/admin/) won't bug you to reschedule until after this date")),
                ('fee', models.IntegerField(null=True, blank=True)),
                ('fee_notes', models.CharField(max_length=256, null=True, blank=True)),
                ('requirements', models.CharField(max_length=256, null=True, blank=True)),
                ('prerequisites', models.CharField(max_length=256, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('short_description', models.TextField(null=True, blank=True)),
                ('safety', models.BooleanField(default=False)),
                ('no_conflict', models.BooleanField(default=False, help_text=b'If true, this class will not raise conflict warnings for events in the same room.')),
                ('max_students', models.IntegerField(default=16)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=('tool.toolsmixin', models.Model),
        ),
        migrations.CreateModel(
            name='CourseCompletion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('quantity', models.IntegerField(default=1)),
                ('completed', models.BooleanField(default=False)),
                ('evaluated', models.BooleanField(default=False)),
                ('emailed', models.BooleanField(default=False)),
                ('evaluation_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('-datetime',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('presentation', models.IntegerField(default=0, help_text=b'Rate the instructor on subject knowledge, pace of the course and communication skills', verbose_name=b'Instructor Presentation', choices=[(1, b'1 - Did not meet expectations'), (2, b'2'), (3, b'3 - Met expectations'), (4, b'4'), (5, b'5 - Exceeded expectations')])),
                ('presentation_comments', models.TextField(blank=True, max_length=512, null=True, verbose_name=b'Comments', validators=[django.core.validators.MaxLengthValidator(512)])),
                ('content', models.IntegerField(default=0, help_text=b'How well did the course content cover the subject area you were interested in?', verbose_name=b'Course Content', choices=[(1, b'1 - Did not meet expectations'), (2, b'2'), (3, b'3 - Met expectations'), (4, b'4'), (5, b'5 - Exceeded expectations')])),
                ('content_comments', models.TextField(blank=True, max_length=512, null=True, verbose_name=b'Comments', validators=[django.core.validators.MaxLengthValidator(512)])),
                ('visuals', models.IntegerField(default=0, help_text=b'How helpful did you find the handouts and audiovisuals presented in this course?', verbose_name=b'Handouts/Audio/Visuals', choices=[(1, b'1 - Did not meet expectations'), (2, b'2'), (3, b'3 - Met expectations'), (4, b'4'), (5, b'5 - Exceeded expectations')])),
                ('visuals_comments', models.TextField(blank=True, max_length=512, null=True, verbose_name=b'Comments', validators=[django.core.validators.MaxLengthValidator(512)])),
                ('question1', models.TextField(null=True, verbose_name=b'What did you like best about this class?', blank=True)),
                ('question2', models.TextField(null=True, verbose_name=b'How could this class be improved?', blank=True)),
                ('question3', models.TextField(null=True, verbose_name=b'What motivated you to take this class?', blank=True)),
                ('question4', models.TextField(null=True, verbose_name=b'What classes would you like to see offered in the future?', blank=True)),
                ('anonymous', models.BooleanField(default=False, help_text=b'If checked your evaluation will be anonymous. If so the staff will not be able to respond to any questions you may have.', verbose_name=b'Evaluate Anonymously')),
            ],
            options={
                'ordering': ('-datetime',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(max_length=255)),
                ('cancelled', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('publish_dt', models.DateTimeField(null=True, blank=True)),
                ('first_date', models.DateTimeField(default=datetime.datetime.now, help_text=b'This will be automatically updated when you save the model. Do not change')),
                ('last_date', models.DateTimeField(default=datetime.datetime.now, help_text=b'This will be automatically updated when you save the model. Do not change')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('time_string', models.CharField(default=b'not implemented', help_text=b'Only used to set dates on creation.', max_length=128)),
                ('branding', models.ForeignKey(blank=True, to='course.Branding', null=True)),
                ('course', models.ForeignKey(blank=True, to='course.Course', null=True)),
            ],
            options={
                'ordering': ('first_date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('order', models.FloatField(default=0)),
                ('parent', models.ForeignKey(blank=True, to='course.Subject', null=True)),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('start', models.DateField()),
                ('end', models.DateField()),
            ],
            options={
                'ordering': ('-start',),
            },
            bases=(models.Model,),
        ),
    ]
