# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0007_auto_20150104_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='picture',
            field=models.ImageField(default=b'profile_images/default_profile_picture.jpg', upload_to=b'profile_images'),
            preserve_default=True,
        ),
    ]
