# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import crop_override.field


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MiscFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=200, editable=False)),
                ('name', models.CharField(max_length=500, null=True, blank=True)),
                ('upload_dt', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(upload_to=b'uploads/file/%Y-%m')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=200, editable=False)),
                ('name', models.CharField(max_length=500, null=True, blank=True)),
                ('upload_dt', models.DateTimeField(auto_now_add=True)),
                ('file', crop_override.field.OriginalImage(max_length=200, null=True, verbose_name=b'Photo', upload_to=b'uploads/photos/%Y-%m')),
                ('caption', models.TextField(null=True, blank=True)),
                ('approved', models.BooleanField(default=False)),
                ('source', models.CharField(default=b'web', max_length=16, choices=[(b'web', b'Web'), (b'instagram', b'Instagram'), (b'twittpic', b'TwittPic'), (b'email', b'Email'), (b'misc', b'Miscelaneous')])),
                ('square_crop', crop_override.field.CropOverride(help_text=b'Usages: Blog Photo, Tool Photo', upload_to=b'uploads/photos/%Y-%m', null=True, verbose_name=b'Square Crop (1:1)', blank=True)),
                ('landscape_crop', crop_override.field.CropOverride(help_text=b'Usages: Featured Blog Photo, Lab Photo', upload_to=b'uploads/photos/%Y-%m', null=True, verbose_name=b'Landscape Crop (3:2)', blank=True)),
                ('portrait_crop', crop_override.field.CropOverride(help_text=b'Usages: None', upload_to=b'uploads/photos/%Y-%m', null=True, verbose_name=b'Portrait Crop (2:3)', blank=True)),
                ('external_url', models.URLField(null=True, blank=True)),
                ('instagramphoto', models.ForeignKey(blank=True, to='instagram.InstagramPhoto', null=True)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhotoTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'ordering': ('-name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaggedFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.IntegerField()),
                ('order', models.IntegerField(default=9999)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('file', models.ForeignKey(to='media.MiscFile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaggedPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.IntegerField()),
                ('order', models.IntegerField(default=9999)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('photo', models.ForeignKey(to='media.Photo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='photo',
            name='tags',
            field=models.ManyToManyField(to='media.PhotoTag', blank=True),
            preserve_default=True,
        ),
    ]
