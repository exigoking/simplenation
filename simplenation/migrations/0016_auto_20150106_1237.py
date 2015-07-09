# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0015_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='definition',
        ),
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
