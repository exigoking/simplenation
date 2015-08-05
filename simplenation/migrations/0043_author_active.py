# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplenation', '0042_pressedtag'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
