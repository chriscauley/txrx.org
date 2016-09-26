# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0004_taggedfile_private'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='instagramphoto',
        ),
        migrations.AlterField(
            model_name='photo',
            name='source',
            field=models.CharField(default=b'web', max_length=16, choices=[(b'web', b'Web'), (b'twittpic', b'TwittPic'), (b'email', b'Email'), (b'misc', b'Miscelaneous')]),
        ),
    ]
