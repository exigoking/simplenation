# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0012_definition_post_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='definition',
            name='last_posted',
            field=models.CharField(default=datetime.datetime(2015, 1, 5, 16, 29, 53, 204091, tzinfo=utc), max_length=128),
            preserve_default=False,
        ),
    ]
