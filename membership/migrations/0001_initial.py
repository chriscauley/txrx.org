# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import wmd.models
import membership.models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=128)),
            ],
            options={
                'ordering': ('text',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LimitedAccessKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=32)),
                ('created', models.DateField(auto_now_add=True)),
                ('expires', models.DateField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MeetingMinutes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=datetime.date.today, unique=True)),
                ('content', wmd.models.MarkDownField()),
                ('member_count', models.IntegerField(default=0, help_text=b'Used only when an exact list of members is unavailable (eg legacy minutes)')),
            ],
            options={
                'ordering': ('-date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('order', models.IntegerField(verbose_name=b'Level')),
                ('discount_percentage', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Membership Level',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MembershipFeature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MembershipGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MembershipRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cost', models.IntegerField()),
                ('months', models.IntegerField(default=1)),
                ('description', models.CharField(max_length=128)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Officer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.CharField(max_length=50)),
                ('start', models.DateField(default=datetime.date.today)),
                ('end', models.DateField(null=True, blank=True)),
                ('order', models.IntegerField(default=999)),
            ],
            options={
                'ordering': ('order', 'end'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=256, null=True, blank=True)),
                ('original', wmd.models.MarkDownField()),
                ('ammended', wmd.models.MarkDownField(null=True, blank=True)),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reasons', models.TextField(blank=True)),
                ('projects', models.TextField(blank=True)),
                ('skills', models.TextField(blank=True)),
                ('expertise', models.TextField(blank=True)),
                ('questions', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UnsubscribeLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=32)),
                ('created', models.DateField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voting_rights', models.BooleanField(default=False)),
                ('suspended', models.BooleanField(default=False)),
                ('waiver', models.FileField(upload_to=b'waivers/', null=True, verbose_name=b'Waivers', blank=True)),
                ('bio', wmd.models.MarkDownField(null=True, blank=True)),
                ('api_key', models.CharField(default=membership.models.rand32, max_length=32)),
                ('by_line', models.CharField(help_text=b'A short description of what you do for the lab.', max_length=50, null=True, blank=True)),
                ('paypal_email', models.EmailField(help_text=b'Leave blank if this is the same as your email address above.', max_length=75, null=True, blank=True)),
                ('notify_global', models.BooleanField(default=True, help_text=b'Uncheck this to stop all email correspondance from this website (same as unchecking all the below items and any future notifications we add).', verbose_name=b'Global Email Preference')),
                ('notify_comments', models.BooleanField(default=True, help_text=b'If checked, you will be emailed whenever someone replies to a comment you make on this site.', verbose_name=b'Comment Response Email')),
                ('notify_classes', models.BooleanField(default=True, help_text=b"If checked, you will be emailed a reminder 24 hours before a class (that you've signed up for).", verbose_name=b'Class Reminder Email')),
                ('notify_sessions', models.BooleanField(default=True, help_text=b'If checked, you will be emailed new class offerings (twice a month).', verbose_name=b'New Course Email')),
                ('membership', models.ForeignKey(default=1, to='membership.Membership')),
                ('photo', models.ForeignKey(blank=True, to='media.Photo', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
