# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.TextField(null=True, blank=True)),
                ('answer', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_name', models.CharField(max_length=128, verbose_name=b'Name')),
                ('from_email', models.EmailField(max_length=75, verbose_name=b'Email')),
                ('message', models.TextField()),
            ],
            options={
                'verbose_name': 'Message',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(help_text=b'Use if desired email is not in a user account. THIS FIELD DOES NOTHING IF THERE IS A USER', max_length=75, null=True, blank=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Person',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=128)),
                ('order', models.IntegerField(default=9999)),
                ('slug', models.CharField(max_length=32)),
                ('person', models.ForeignKey(to='contact.Person')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Subject',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubjectFAQ',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0)),
                ('faq', models.ForeignKey(to='contact.FAQ')),
                ('subject', models.ForeignKey(to='contact.Subject')),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='message',
            name='subject',
            field=models.ForeignKey(to='contact.Subject'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
