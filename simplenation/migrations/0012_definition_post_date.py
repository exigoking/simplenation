# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0011_remove_definition_post_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='definition',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 5, 16, 27, 45, 215604, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
