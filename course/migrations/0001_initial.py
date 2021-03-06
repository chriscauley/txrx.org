# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-04-19 12:23
from __future__ import unicode_literals

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import lablackey.db.models
import media.models
import tool.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('drop', '0006_auto_20170211_2031'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('image', models.ImageField(upload_to=b'course_branding/%Y-%m')),
                ('small_image_override', models.ImageField(blank=True, null=True, upload_to=b'course_branding/%Y-%m')),
            ],
        ),
        migrations.CreateModel(
            name='ClassTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('end_time', models.TimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('emailed', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ('start',),
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('active', models.BooleanField(default=True)),
                ('short_name', models.CharField(blank=True, help_text=b'Used for the events page.', max_length=64, null=True)),
                ('no_discount', models.BooleanField(default=False)),
                ('presentation', models.BooleanField(default=True, verbose_name=b'Evaluate Presentation')),
                ('visuals', models.BooleanField(default=True, verbose_name=b'Evaluate Visuals')),
                ('content', models.BooleanField(default=True, verbose_name=b'Evaluate Content')),
                ('reschedule_on', models.DateField(default=datetime.date.today, help_text=b"The dashboard (/admin/) won't bug you to reschedule until after this date")),
                ('fee', models.IntegerField(blank=True, default=0, null=True)),
                ('fee_notes', models.CharField(blank=True, max_length=256, null=True)),
                ('requirements', models.CharField(blank=True, max_length=256, null=True)),
                ('prerequisites', models.CharField(blank=True, max_length=256, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('short_description', models.TextField(blank=True, null=True)),
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
            name='CourseEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[(b'new', b'New'), (b'failed', b'Failed'), (b'completed', b'Completed'), (b'incomplete', b'Incomplete')], default=b'new', max_length=16)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('status_changed', models.DateTimeField(default=django.utils.timezone.now)),
                ('quantity', models.IntegerField(default=1)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CourseRoomTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours_at', models.FloatField(default=0, help_text=b'Number of hours at location. 0 = Until class ends.')),
                ('day', models.IntegerField(choices=[(0, b'All'), (1, b'Day 1'), (2, b'Day 2'), (3, b'Day 3'), (4, b'Day 4'), (5, b'Day 5')], default=0)),
                ('order', models.IntegerField(default=999)),
            ],
            options={
                'ordering': ('day', 'order'),
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[(b'new', b'New'), (b'failed', b'Failed'), (b'completed', b'Completed'), (b'incomplete', b'Incomplete')], default=b'new', max_length=16)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('status_changed', models.DateTimeField(default=django.utils.timezone.now)),
                ('quantity', models.IntegerField(default=0)),
                ('evaluated', models.BooleanField(default=False)),
                ('emailed', models.BooleanField(default=False)),
                ('evaluation_date', models.DateTimeField(blank=True, null=True)),
                ('transaction_ids', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ('-datetime',),
            },
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('presentation', models.IntegerField(choices=[(1, b'1 - Did not meet expectations'), (2, b'2'), (3, b'3 - Met expectations'), (4, b'4'), (5, b'5 - Exceeded expectations')], default=0, help_text=b'Rate the instructor on subject knowledge, pace of the course and communication skills', verbose_name=b'Instructor Presentation')),
                ('presentation_comments', models.TextField(blank=True, max_length=512, null=True, validators=[django.core.validators.MaxLengthValidator(512)], verbose_name=b'Comments')),
                ('content', models.IntegerField(choices=[(1, b'1 - Did not meet expectations'), (2, b'2'), (3, b'3 - Met expectations'), (4, b'4'), (5, b'5 - Exceeded expectations')], default=0, help_text=b'How well did the course content cover the subject area you were interested in?', verbose_name=b'Course Content')),
                ('content_comments', models.TextField(blank=True, max_length=512, null=True, validators=[django.core.validators.MaxLengthValidator(512)], verbose_name=b'Comments')),
                ('visuals', models.IntegerField(choices=[(1, b'1 - Did not meet expectations'), (2, b'2'), (3, b'3 - Met expectations'), (4, b'4'), (5, b'5 - Exceeded expectations')], default=0, help_text=b'How helpful did you find the handouts and audio visuals presented in this course?', verbose_name=b'Handouts/Audio/Visuals')),
                ('visuals_comments', models.TextField(blank=True, max_length=512, null=True, validators=[django.core.validators.MaxLengthValidator(512)], verbose_name=b'Comments')),
                ('question1', models.TextField(blank=True, null=True, verbose_name=b'What did you like best about this class?')),
                ('question2', models.TextField(blank=True, null=True, verbose_name=b'How could this class be improved?')),
                ('question3', models.TextField(blank=True, null=True, verbose_name=b'What motivated you to take this class?')),
                ('question4', models.TextField(blank=True, null=True, verbose_name=b'What classes would you like to see offered in the future?')),
                ('anonymous', models.BooleanField(default=False, help_text=b'If checked your evaluation will be anonymous. If so the staff will not be able to respond to any questions you may have.', verbose_name=b'Evaluate Anonymously')),
            ],
            options={
                'ordering': ('-datetime',),
            },
            bases=(models.Model, lablackey.db.models.JsonMixin),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('cancelled', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('overbook', models.IntegerField(default=0, help_text=b'This session will not appear as overbooked if it is less than X seats overbooked.')),
                ('private', models.BooleanField(default=False, help_text=b'Private classes cannot be signed up for and do not appear on the session page unless the user is manually enrolled. It will appear on calendar but it will be marked in red.')),
                ('notified', models.DateTimeField(blank=True, null=True)),
                ('publish_dt', models.DateTimeField(blank=True, null=True)),
                ('first_date', models.DateTimeField(default=datetime.datetime.now, help_text=b'This will be automatically updated when you save the model. Do not change')),
                ('last_date', models.DateTimeField(default=datetime.datetime.now, help_text=b'This will be automatically updated when you save the model. Do not change')),
                ('instructor_completed', models.DateField(blank=True, null=True)),
                ('needed', models.TextField(blank=True, default=b'', verbose_name=b'What is needed?')),
                ('needed_completed', models.DateField(blank=True, null=True)),
                ('branding', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.Branding')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course')),
            ],
            options={
                'ordering': ('first_date',),
            },
            bases=(media.models.PhotosMixin, models.Model, lablackey.db.models.JsonMixin),
        ),
        migrations.CreateModel(
            name='SessionProduct',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='drop.Product')),
                ('session', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='course.Session')),
            ],
            bases=('drop.product',),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('order', models.FloatField(default=0)),
                ('level', models.IntegerField(default=0)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.Subject')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('start', models.DateField()),
                ('end', models.DateField()),
            ],
            options={
                'ordering': ('-start',),
            },
        ),
    ]
