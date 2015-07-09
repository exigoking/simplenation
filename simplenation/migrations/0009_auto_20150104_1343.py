# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0008_auto_20150104_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='picture',
            field=models.ImageField(default=b'profile_images/thomas_party_6.jpg', upload_to=b'profile_images'),
            preserve_default=True,
        ),
    ]
