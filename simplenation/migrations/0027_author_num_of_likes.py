# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0026_auto_20150118_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='num_of_likes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
