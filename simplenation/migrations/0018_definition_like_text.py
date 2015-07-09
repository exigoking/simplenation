# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0017_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='definition',
            name='like_text',
            field=models.CharField(default=b'Like', max_length=128),
            preserve_default=True,
        ),
    ]
