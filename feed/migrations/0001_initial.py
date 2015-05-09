# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FeedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('thumbnail', models.ImageField(default=b'feed_thumbnails/default.png', upload_to=b'feed_thumbnails')),
                ('item_type', models.CharField(max_length=16, choices=[(b'blog', b'Blog Post'), (b'session', b'Class'), (b'event', b'Event'), (b'thing', b'Thing'), (b'video', b'Video'), (b'link', b'Link'), (b'other', b'Other')])),
                ('publish_dt', models.DateTimeField()),
                ('get_absolute_url', models.CharField(max_length=256)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('votes', models.IntegerField(default=0)),
                ('featured', models.BooleanField(default=False)),
                ('object_id', models.PositiveIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feed_item', models.ForeignKey(to='feed.FeedItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
