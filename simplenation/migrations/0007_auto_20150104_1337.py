# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0006_auto_20141231_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='picture',
            field=models.ImageField(default=b'/Users/timurmalgazhdarov/Sites/djangobook.com/media/profile_images/default_profile_picture.jpg', upload_to=b'profile_images'),
            preserve_default=True,
        ),
    ]
