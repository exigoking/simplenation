# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0024_auto_20150118_0849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='score',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
    ]
