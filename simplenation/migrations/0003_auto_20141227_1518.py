# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0002_auto_20141227_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='slug',
            field=models.SlugField(default='defualt', unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='term',
            name='slug',
            field=models.SlugField(default='default', unique=True),
            preserve_default=False,
        ),
    ]
