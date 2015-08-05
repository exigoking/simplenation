# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0039_auto_20150724_0636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='picture',
            field=imagekit.models.fields.ProcessedImageField(default=b'profile_images/default_profile_picture.png', upload_to=b'profile_images'),
        ),
    ]
