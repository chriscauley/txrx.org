# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.files.storage
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={b'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator(b'^[\\w\\.+-]+$', 'Enter a valid username. This value may contain only letters, numbers and ./+/-/_ characters.', b'invalid')], help_text='Required. 30 characters or fewer. Letters, digits, and ./+/-/_ only.', unique=True, verbose_name='username')),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='email address')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_toolmaster', models.BooleanField(default=False, help_text=b'Toolmasters can give any user access to any Tool Criteria.')),
                ('is_gatekeeper', models.BooleanField(default=False, help_text=b'Gatekeepers have 24/7 building access.')),
                ('is_shopkeeper', models.BooleanField(default=False, help_text=b'Shopkeepers can mark receipts as received.')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('paypal_email', models.EmailField(max_length=255, null=True, blank=True)),
                ('id_photo_date', models.DateTimeField(null=True, blank=True)),
                ('headshot', models.FileField(upload_to=b'%Y%m', storage=django.core.files.storage.FileSystemStorage(base_url=b'/staff_only/', location=b'/home/chriscauley/txrx.org/main/../.staff'), max_length=200, blank=True, null=True, verbose_name=b'Head Shot')),
                ('orientation_status', models.CharField(default=b'new', max_length=32, choices=[(b'new', b'New'), (b'emailed', b'Emailed'), (b'scheduled', b'scheduled'), (b'oriented', b'Oriented')])),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'ordering': ('username',),
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='RFID',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(unique=True, max_length=16)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserCheckin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_in', models.DateTimeField(auto_now_add=True)),
                ('time_out', models.DateTimeField(null=True, blank=True)),
                ('object_id', models.IntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('note', models.CharField(max_length=256)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
