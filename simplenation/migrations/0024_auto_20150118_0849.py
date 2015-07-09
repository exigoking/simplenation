# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0023_definition_reporter'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='rank',
            field=models.IntegerField(default=9999999),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='author',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
