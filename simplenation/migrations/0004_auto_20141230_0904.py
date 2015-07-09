# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0003_auto_20141227_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='picture',
            field=models.ImageField(upload_to=b'/Users/timurmalgazhdarov/Sites/djangobook.com/media/profile_images', blank=True),
            preserve_default=True,
        ),
    ]
