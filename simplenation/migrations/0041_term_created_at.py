# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0040_auto_20150801_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='term',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 2, 10, 10, 42, 62111, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
