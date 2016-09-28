# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import tool.models
import media.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('image', models.ImageField(upload_to=b'course_branding/%Y-%m')),
                ('small_image_override', models.ImageField(null=True, upload_to=b'course_branding/%Y-%m', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClassTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField()),
                ('end_time', models.TimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('emailed', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('start',),
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('active', models.BooleanField(default=True)),
                ('short_name', models.CharField(help_text=b'Used for the events page.', max_length=64, null=True, blank=True)),
                ('no_discount', models.BooleanField(default=False)),
                ('presentation', models.BooleanField(default=True, verbose_name=b'Evaluate Presentation')),
                ('visuals', models.BooleanField(default=True, verbose_name=b'Evaluate Visuals')),
                ('content', models.BooleanField(default=True, verbose_name=b'Evaluate Content')),
                ('reschedule_on', models.DateField(default=datetime.date.today, help_text=b"The dashboard (/admin/) won't bug you to reschedule until after this date")),
                ('fee', models.IntegerField(default=0, null=True, blank=True)),
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
            bases=(media.models.PhotosMixin, tool.models.ToolsMixin, media.models.FilesMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CourseRoomTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hours_at', models.FloatField(default=0, help_text=b'Number of hours at location. 0 = Until class ends.')),
                ('day', models.IntegerField(default=0, choices=[(0, b'All'), (1, b'Day 1'), (2, b'Day 2'), (3, b'Day 3'), (4, b'Day 4'), (5, b'Day 5')])),
                ('order', models.IntegerField(default=999)),
            ],
            options={
                'ordering': ('day', 'order'),
            },
        ),
        migrations.CreateModel(
            name='CourseSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('completed', models.DateTimeField(null=True, blank=True)),
                ('quantity', models.IntegerField(default=1)),
                ('evaluated', models.BooleanField(default=False)),
                ('emailed', models.BooleanField(default=False)),
                ('evaluation_date', models.DateTimeField(null=True, blank=True)),
                ('transaction_ids', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ('-datetime',),
            },
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
                ('visuals', models.IntegerField(default=0, help_text=b'How helpful did you find the handouts and audio visuals presented in this course?', verbose_name=b'Handouts/Audio/Visuals', choices=[(1, b'1 - Did not meet expectations'), (2, b'2'), (3, b'3 - Met expectations'), (4, b'4'), (5, b'5 - Exceeded expectations')])),
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
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cancelled', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('private', models.BooleanField(default=False, help_text=b'Private classes cannot be signed up for and do not appear on the session page unless the user is manually enrolled. It will appear on calendar but it will be marked in red.')),
                ('notified', models.DateTimeField(null=True, blank=True)),
                ('publish_dt', models.DateTimeField(null=True, blank=True)),
                ('first_date', models.DateTimeField(default=datetime.datetime.now, help_text=b'This will be automatically updated when you save the model. Do not change')),
                ('last_date', models.DateTimeField(default=datetime.datetime.now, help_text=b'This will be automatically updated when you save the model. Do not change')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('needed', models.TextField(default=b'', verbose_name=b'What is needed?', blank=True)),
                ('needed_completed', models.DateField(null=True, blank=True)),
                ('branding', models.ForeignKey(blank=True, to='course.Branding', null=True)),
                ('course', models.ForeignKey(to='course.Course')),
            ],
            options={
                'ordering': ('first_date',),
            },
            bases=(media.models.PhotosMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('order', models.FloatField(default=0)),
                ('level', models.IntegerField(default=0)),
                ('parent', models.ForeignKey(blank=True, to='course.Subject', null=True)),
            ],
            options={
                'ordering': ('order',),
            },
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
        ),
    ]
