# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0004_auto_20141230_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='picture',
            field=models.ImageField(upload_to=b'profile_images', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='definition',
            name='body',
            field=models.TextField(max_length=512),
            preserve_default=True,
        ),
    ]
