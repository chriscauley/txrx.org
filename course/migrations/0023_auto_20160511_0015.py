# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0002_auto_20150614_1510'),
        ('course', '0022_course_no_discount'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseRoomTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.TimeField()),
                ('day', models.IntegerField(default=0, choices=[(0, b'All'), (1, b'Day 1'), (2, b'Day 2'), (3, b'Day 3'), (4, b'Day 4'), (5, b'Day 5')])),
                ('course', models.ForeignKey(to='course.Course')),
                ('room', models.ForeignKey(to='geo.Room')),
            ],
            options={
                'ordering': ('day', 'time'),
            },
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='visuals',
            field=models.IntegerField(default=0, help_text=b'How helpful did you find the handouts and audio visuals presented in this course?', verbose_name=b'Handouts/Audio/Visuals', choices=[(1, b'1 - Did not meet expectations'), (2, b'2'), (3, b'3 - Met expectations'), (4, b'4'), (5, b'5 - Exceeded expectations')]),
        ),
    ]
